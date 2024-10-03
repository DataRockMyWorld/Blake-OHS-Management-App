import pyotp
import time 
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings
from .models import oneTimePassword




def send_otp_to_user(email):
    """
    Send OTP to user's email
    """
    subject = "Your One Time Password (OTP) for Blake-OHS-Management-App"
    secret_key = pyotp.random_base32()
    otp = pyotp.TOTP(secret_key, digits=6, interval=500)
    otp_code = otp.now()
    user = get_user_model().objects.get(email=email)
    current_site= "mysite.com"
    message = f"Hi {user.first_name}, thanks for signing up on {current_site}. Your OTP is {otp_code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    
    oneTimePassword.objects.create(
        user=user,
        code=otp_code
    )
    
    d_email = EmailMessage(subject, message, from_email, [email])
    d_email.send(fail_silently=True)

def send_normal_email(data):
    """
    Send normal email
    """
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']],
    )
    email.send()
