from main.celery import app
from django.core.mail import send_mail

@app.task(name='send-email-about-board-task')
def notification_email(user_name, board, emails):
    send_mail(
        subject="New Board",
        message=f"{user_name} have added you to a new board: {board}",
        from_email = "trelloclone1@gmail.com",
        recipient_list=emails,
        fail_silently = False
    )