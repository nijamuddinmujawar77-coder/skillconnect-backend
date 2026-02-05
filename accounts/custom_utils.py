"""
Custom utility functions for the accounts app
"""

def calculate_profile_strength(user):
    """
    Calculate the profile completion strength for a user
    Returns a percentage (0-100) based on filled profile fields
    """
    strength = 0
    total_fields = 10  # Total fields to check
    
    # Basic info checks
    if user.first_name:
        strength += 10
    if user.last_name:
        strength += 10
    if user.email:
        strength += 10
    if hasattr(user, 'profile_picture') and user.profile_picture:
        strength += 10
    
    # Check for work experience
    if hasattr(user, 'workexperience_set') and user.workexperience_set.exists():
        strength += 20
    
    # Check for education
    if hasattr(user, 'education_set') and user.education_set.exists():
        strength += 20
    
    # Check for skills
    if hasattr(user, 'skill_set') and user.skill_set.exists():
        strength += 20
    
    return min(strength, 100)


def get_user_activity_level(user):
    """
    Determine user activity level based on profile completeness and usage
    Returns: 'low', 'medium', or 'high'
    """
    profile_strength = calculate_profile_strength(user)
    
    if profile_strength >= 80:
        return 'high'
    elif profile_strength >= 50:
        return 'medium'
    else:
        return 'low'


# Custom error messages for the application
CUSTOM_ERROR_MESSAGES = {
    'required': 'This field is required.',
    'invalid': 'Please enter a valid value.',
    'max_length': 'This field cannot exceed {max_length} characters.',
    'min_length': 'This field must be at least {min_length} characters long.',
    'unique': 'This value already exists. Please choose a different one.',
    'email_invalid': 'Please enter a valid email address.',
    'password_too_common': 'This password is too common. Please choose a more secure password.',
    'password_too_short': 'Password must be at least 8 characters long.',
    'password_mismatch': 'Passwords do not match.',
    'user_not_found': 'User not found.',
    'invalid_credentials': 'Invalid email or password.',
    'account_disabled': 'Your account has been disabled.',
    'profile_incomplete': 'Please complete your profile to access this feature.',
    'unauthorized': 'You are not authorized to perform this action.',
    'file_too_large': 'File size cannot exceed 5MB.',
    'invalid_file_type': 'Only image files (PNG, JPG, JPEG) are allowed.',
}