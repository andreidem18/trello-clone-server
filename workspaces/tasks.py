from main.celery import app
from django.core.mail import send_mail

@app.task(name='send-notification-email-task')
def notification_email(user_name, workspace, emails):
    send_mail(
        subject="New Workspace",
        message=f"{user_name} have added you to a new Workspace: {workspace}",
        from_email = "trelloclone1@gmail.com",
        recipient_list=emails,
        fail_silently = False
    )