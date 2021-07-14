from main.celery import app
from django.core.mail import send_mail

@app.task(name='send-email-about welcome')
def notification_email(user_name, email):
    send_mail(
        subject="Welcome",
        message=f"Hello {user_name}! Welcome to the Trello Team :)",
        from_email = "trelloclone1@gmail.com",
        recipient_list=[email],
        fail_silently = False
    )