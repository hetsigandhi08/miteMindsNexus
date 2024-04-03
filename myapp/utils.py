# your_app/utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_forgot_password_mail(user, token):
    subject = 'Reset Your Password'
    message = f'Hi {user.username},\n\nPlease click the following link to reset your password:\n\n{settings.BASE_URL}/reset-password/{token}/\n\nIf you did not request a password reset, please ignore this email.\n\nThank you,\nYourAppName Team'
    sender_email = settings.EMAIL_HOST_USER
    recipient_email = user.email

    send_mail(subject, message, sender_email, [recipient_email])
