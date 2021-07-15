from notifications.serializer import NotificationSerializer
from main.celery import app
from django.core.mail import send_mail

@app.task(name='notify deadline')
def notificate_deadline(members, card, img):
    # Notifications
    emails = []
    for member in members:
        emails.append(member['email'])
        new_notification = {
            'text': f"The time to finish the tasks from the card {card} have ended",
            'url': '',
            'img_url': img,
            'user': member['id']
        }
        serialized = NotificationSerializer(data=new_notification)
        serialized.is_valid()
        serialized.save()

    # Emails
    send_mail(
        subject="Tasks ended",
        message=f"The time to finish the tasks from the card {card} have ended",
        from_email = "trelloclone1@gmail.com",
        recipient_list=emails,
        fail_silently = False
    )