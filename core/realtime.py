"""
SkillConnect - Real-time Features Module
WebSocket Integration for Live Notifications & Real-time Updates
"""

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time notifications"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope["user"]
        
        # Only allow authenticated users
        if self.user == AnonymousUser:
            await self.close()
            return
        
        # Create user-specific group
        self.notification_group = f"notifications_{self.user.id}"
        
        # Join notification group
        await self.channel_layer.group_add(
            self.notification_group,
            self.channel_name
        )
        
        # Accept connection
        await self.accept()
        
        # Mark user as online
        await self.update_user_status(online=True)
        
        # Send initial data
        await self.send_initial_notifications()
        
        logger.info(f"User {self.user.email} connected to notifications")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'notification_group'):
            # Leave notification group
            await self.channel_layer.group_discard(
                self.notification_group,
                self.channel_name
            )
        
        # Mark user as offline
        if hasattr(self, 'user') and self.user != AnonymousUser:
            await self.update_user_status(online=False)
            logger.info(f"User {self.user.email} disconnected from notifications")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'mark_notification_read':
                await self.mark_notification_read(data.get('notification_id'))
            elif message_type == 'get_online_users':
                await self.send_online_users()
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': datetime.now().isoformat()
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON data'
            }))
    
    async def send_initial_notifications(self):
        """Send initial notifications when user connects"""
        # Get unread notifications from database
        notifications = await self.get_user_notifications()
        
        await self.send(text_data=json.dumps({
            'type': 'initial_notifications',
            'notifications': notifications,
            'count': len([n for n in notifications if not n['read']])
        }))
    
    async def notification_message(self, event):
        """Handle notification message from group"""
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'notification': event['notification']
        }))
    
    async def job_alert(self, event):
        """Handle job alert notification"""
        await self.send(text_data=json.dumps({
            'type': 'job_alert',
            'job': event['job'],
            'message': f"New job match found: {event['job']['title']}"
        }))
    
    async def application_update(self, event):
        """Handle job application status update"""
        await self.send(text_data=json.dumps({
            'type': 'application_update',
            'application': event['application'],
            'message': f"Application status updated: {event['application']['status']}"
        }))
    
    @sync_to_async
    def get_user_notifications(self):
        """Get user notifications from database"""
        # This would fetch from your notification model
        # For now, returning mock data
        return [
            {
                'id': 1,
                'title': 'Welcome to SkillConnect!',
                'message': 'Complete your profile to get better job matches',
                'type': 'welcome',
                'read': False,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'title': 'New Job Match',
                'message': 'We found 3 jobs that match your skills',
                'type': 'job_match',
                'read': False,
                'created_at': (datetime.now() - timedelta(hours=2)).isoformat()
            }
        ]
    
    @sync_to_async
    def mark_notification_read(self, notification_id: int):
        """Mark notification as read in database"""
        # This would update notification in database
        logger.info(f"Marking notification {notification_id} as read for user {self.user.id}")
    
    async def update_user_status(self, online: bool):
        """Update user online status"""
        status_key = f"user_status:{self.user.id}"
        
        if online:
            cache.set(status_key, {
                'online': True,
                'last_seen': datetime.now().isoformat(),
                'socket_id': self.channel_name
            }, timeout=300)  # 5 minutes timeout
        else:
            cache.set(status_key, {
                'online': False,
                'last_seen': datetime.now().isoformat()
            }, timeout=86400)  # Keep offline status for 24 hours
    
    async def send_online_users(self):
        """Send list of online users"""
        online_users = await self.get_online_users()
        
        await self.send(text_data=json.dumps({
            'type': 'online_users',
            'users': online_users
        }))
    
    async def get_online_users(self):
        """Get list of online users"""
        # This would query cache for online users
        # Mock implementation
        return [
            {'id': 1, 'name': 'John Doe', 'status': 'online'},
            {'id': 2, 'name': 'Jane Smith', 'status': 'online'}
        ]

class JobAlertService:
    """Service for managing real-time job alerts"""
    
    @staticmethod
    async def send_job_alert(user_id: int, job_data: Dict[str, Any]):
        """Send job alert to specific user"""
        channel_layer = get_channel_layer()
        group_name = f"notifications_{user_id}"
        
        await channel_layer.group_send(group_name, {
            'type': 'job_alert',
            'job': job_data
        })
    
    @staticmethod
    async def broadcast_new_job(job_data: Dict[str, Any]):
        """Broadcast new job to all relevant users"""
        channel_layer = get_channel_layer()
        
        # This would query users interested in this job type/location
        interested_users = await JobAlertService.get_interested_users(job_data)
        
        for user_id in interested_users:
            await JobAlertService.send_job_alert(user_id, job_data)
    
    @staticmethod
    async def get_interested_users(job_data: Dict[str, Any]) -> List[int]:
        """Get users interested in this type of job"""
        # Mock implementation - would query user preferences
        return [1, 2, 3]  # User IDs

class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    async def send_notification(user_id: int, notification: Dict[str, Any]):
        """Send notification to specific user"""
        channel_layer = get_channel_layer()
        group_name = f"notifications_{user_id}"
        
        # Save notification to database first
        await NotificationService.save_notification(user_id, notification)
        
        # Send via WebSocket
        await channel_layer.group_send(group_name, {
            'type': 'notification_message',
            'notification': notification
        })
    
    @staticmethod
    @sync_to_async
    def save_notification(user_id: int, notification: Dict[str, Any]):
        """Save notification to database"""
        # This would save to your notification model
        logger.info(f"Saving notification for user {user_id}: {notification['title']}")
    
    @staticmethod
    async def send_welcome_notification(user_id: int, user_name: str):
        """Send welcome notification to new user"""
        notification = {
            'id': None,  # Will be set after saving
            'title': f'Welcome to SkillConnect, {user_name}!',
            'message': 'Complete your profile to get personalized job recommendations',
            'type': 'welcome',
            'read': False,
            'created_at': datetime.now().isoformat(),
            'actions': [
                {
                    'label': 'Complete Profile',
                    'url': '/profile.html'
                }
            ]
        }
        
        await NotificationService.send_notification(user_id, notification)
    
    @staticmethod
    async def send_job_application_update(user_id: int, application_data: Dict[str, Any]):
        """Send job application status update"""
        notification = {
            'id': None,
            'title': 'Application Status Update',
            'message': f'Your application for {application_data["job_title"]} has been {application_data["status"]}',
            'type': 'application_update',
            'read': False,
            'created_at': datetime.now().isoformat(),
            'data': application_data
        }
        
        await NotificationService.send_notification(user_id, notification)

class LiveActivityService:
    """Service for live activity updates"""
    
    @staticmethod
    async def track_user_activity(user_id: int, activity: str, data: Dict[str, Any]):
        """Track and broadcast user activity"""
        activity_data = {
            'user_id': user_id,
            'activity': activity,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache recent activity
        activity_key = f"user_activity:{user_id}"
        recent_activities = cache.get(activity_key, [])
        recent_activities.append(activity_data)
        
        # Keep only last 10 activities
        recent_activities = recent_activities[-10:]
        cache.set(activity_key, recent_activities, timeout=3600)
        
        # Broadcast to admin/analytics
        channel_layer = get_channel_layer()
        await channel_layer.group_send("admin_dashboard", {
            'type': 'user_activity',
            'activity': activity_data
        })

# WebSocket routing configuration
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

# Frontend JavaScript Integration
FRONTEND_WEBSOCKET_CODE = """
// Real-time WebSocket Integration for SkillConnect Frontend

class SkillConnectWebSocket {
    constructor(userId) {
        this.userId = userId;
        this.socket = null;
        this.reconnectInterval = null;
        this.notifications = [];
        this.onlineUsers = [];
        
        this.connect();
        this.setupEventHandlers();
    }
    
    connect() {
        const token = localStorage.getItem('access_token');
        const wsUrl = `ws://localhost:8000/ws/notifications/?token=${token}`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = (event) => {
            console.log('✅ WebSocket connected');
            this.clearReconnectInterval();
            this.updateConnectionStatus(true);
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.socket.onclose = (event) => {
            console.log('❌ WebSocket disconnected');
            this.updateConnectionStatus(false);
            this.startReconnecting();
        };
        
        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }
    
    handleMessage(data) {
        switch(data.type) {
            case 'initial_notifications':
                this.notifications = data.notifications;
                this.updateNotificationUI();
                break;
                
            case 'new_notification':
                this.notifications.unshift(data.notification);
                this.showNotificationToast(data.notification);
                this.updateNotificationUI();
                break;
                
            case 'job_alert':
                this.showJobAlert(data.job);
                break;
                
            case 'application_update':
                this.showApplicationUpdate(data.application);
                break;
                
            case 'online_users':
                this.onlineUsers = data.users;
                this.updateOnlineUsersUI();
                break;
        }
    }
    
    showNotificationToast(notification) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'notification-toast';
        toast.innerHTML = `
            <div class="toast-header">
                <strong>${notification.title}</strong>
                <button onclick="this.parentElement.parentElement.remove()">&times;</button>
            </div>
            <div class="toast-body">${notification.message}</div>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
    
    showJobAlert(job) {
        const alert = `
            <div class="job-alert-modal">
                <div class="job-alert-content">
                    <h3>🚀 New Job Match!</h3>
                    <h4>${job.title}</h4>
                    <p><strong>Company:</strong> ${job.company}</p>
                    <p><strong>Location:</strong> ${job.location}</p>
                    <div class="job-alert-actions">
                        <button onclick="viewJob(${job.id})">View Job</button>
                        <button onclick="closeJobAlert()">Later</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', alert);
    }
    
    updateNotificationUI() {
        const notificationCount = this.notifications.filter(n => !n.read).length;
        
        // Update notification badge
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            badge.textContent = notificationCount;
            badge.style.display = notificationCount > 0 ? 'block' : 'none';
        }
        
        // Update notification dropdown
        this.renderNotificationDropdown();
    }
    
    renderNotificationDropdown() {
        const dropdown = document.querySelector('.notification-dropdown');
        if (!dropdown) return;
        
        dropdown.innerHTML = this.notifications.length > 0 ? 
            this.notifications.map(n => `
                <div class="notification-item ${n.read ? 'read' : 'unread'}" data-id="${n.id}">
                    <div class="notification-title">${n.title}</div>
                    <div class="notification-message">${n.message}</div>
                    <div class="notification-time">${this.formatTime(n.created_at)}</div>
                </div>
            `).join('') :
            '<div class="no-notifications">No notifications</div>';
    }
    
    markAsRead(notificationId) {
        this.socket.send(JSON.stringify({
            type: 'mark_notification_read',
            notification_id: notificationId
        }));
        
        // Update local state
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
            notification.read = true;
            this.updateNotificationUI();
        }
    }
    
    startReconnecting() {
        this.reconnectInterval = setInterval(() => {
            console.log('🔄 Attempting to reconnect...');
            this.connect();
        }, 5000);
    }
    
    clearReconnectInterval() {
        if (this.reconnectInterval) {
            clearInterval(this.reconnectInterval);
            this.reconnectInterval = null;
        }
    }
    
    updateConnectionStatus(connected) {
        const statusEl = document.querySelector('.connection-status');
        if (statusEl) {
            statusEl.className = `connection-status ${connected ? 'connected' : 'disconnected'}`;
            statusEl.textContent = connected ? '🟢 Connected' : '🔴 Disconnected';
        }
    }
    
    setupEventHandlers() {
        // Notification dropdown toggle
        document.addEventListener('click', (e) => {
            if (e.target.matches('.notification-bell')) {
                document.querySelector('.notification-dropdown').classList.toggle('show');
            }
            
            if (e.target.matches('.notification-item')) {
                const notificationId = parseInt(e.target.dataset.id);
                this.markAsRead(notificationId);
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.notification-container')) {
                document.querySelector('.notification-dropdown')?.classList.remove('show');
            }
        });
    }
    
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return date.toLocaleDateString();
    }
}

// Initialize WebSocket when user is authenticated
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (token) {
        // Get user ID from token or API call
        const userId = getUserIdFromToken(token);
        window.skillConnectWS = new SkillConnectWebSocket(userId);
    }
});

// CSS for notifications
const notificationStyles = `
<style>
.notification-container {
    position: relative;
    display: inline-block;
}

.notification-bell {
    position: relative;
    cursor: pointer;
    font-size: 20px;
    color: var(--primary-teal);
}

.notification-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background: #e74c3c;
    color: white;
    border-radius: 50%;
    padding: 2px 6px;
    font-size: 12px;
    font-weight: bold;
    min-width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.notification-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    width: 350px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    max-height: 400px;
    overflow-y: auto;
    display: none;
}

.notification-dropdown.show {
    display: block;
}

.notification-item {
    padding: 12px 16px;
    border-bottom: 1px solid #f0f0f0;
    cursor: pointer;
    transition: background-color 0.2s;
}

.notification-item:hover {
    background: #f8f9fa;
}

.notification-item.unread {
    background: #e3f2fd;
    border-left: 3px solid var(--primary-teal);
}

.notification-title {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.notification-message {
    color: var(--gray-600);
    font-size: 14px;
    margin-bottom: 4px;
}

.notification-time {
    color: var(--gray-500);
    font-size: 12px;
}

.notification-toast {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 9999;
    min-width: 300px;
    animation: slideIn 0.3s ease;
}

.toast-header {
    background: var(--primary-teal);
    color: white;
    padding: 8px 12px;
    border-radius: 8px 8px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.toast-body {
    padding: 12px;
    color: var(--text-primary);
}

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.connection-status {
    font-size: 12px;
    padding: 4px 8px;
    border-radius: 4px;
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1000;
}

.connection-status.connected {
    background: #d4edda;
    color: #155724;
}

.connection-status.disconnected {
    background: #f8d7da;
    color: #721c24;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', notificationStyles);
"""

# Installation instructions for channels
"""
# Add to requirements.txt:
channels==4.0.0
channels-redis==4.1.0
redis==5.0.1

# Add to settings.py:
INSTALLED_APPS = [
    # ... other apps
    'channels',
]

ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Update asgi.py:
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from core.realtime import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
"""