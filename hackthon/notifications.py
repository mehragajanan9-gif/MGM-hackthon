from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

# Email Notification (optional, if citizen email is stored in User model)
def send_status_update_email(complaint, status):
    user_email = complaint.citizen.email  # Django User model email
    if not user_email:
        return
    subject = f"Complaint #{complaint.id} Status Update"
    message = (
        f"Hello {complaint.citizen.username},\n\n"
        f"Your complaint '{complaint.title}' has been updated to status: {status}.\n"
        f"AI Summary: {complaint.ai_summary}\n\n"
        f"Thank you,\nJanSahayak AI"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])


# SMS Notification (Citizen Profile.phone)
def send_sms_notification(complaint, status):
    phone_number = complaint.citizen.profile.phone
    if not phone_number:
        return
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"Complaint #{complaint.id} updated to {status}. AI Summary: {complaint.ai_summary}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )


# WhatsApp Notification (Citizen + Admin Emergency)
def send_whatsapp_notification(complaint, status, emergency=False):
    phone_number = complaint.citizen.profile.phone
    if not phone_number:
        return
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    if emergency:
        body = (
            f"🚨 EMERGENCY ALERT 🚨\n"
            f"Complaint #{complaint.id} flagged as emergency!\n"
            f"Department: {complaint.department}\n"
            f"Summary: {complaint.ai_summary}"
        )
        # Send to Admin
        client.messages.create(
            body=body,
            from_="whatsapp:" + settings.TWILIO_WHATSAPP_NUMBER,
            to="whatsapp:" + settings.ADMIN_PHONE_NUMBER
        )
    else:
        body = (
            f"Complaint #{complaint.id} updated to {status}.\n"
            f"AI Summary: {complaint.ai_summary}"
        )
        # Send to Citizen
        client.messages.create(
            body=body,
            from_="whatsapp:" + settings.TWILIO_WHATSAPP_NUMBER,
            to="whatsapp:" + phone_number
        )


# Centralized Trigger
def notify_citizen_and_admin(complaint, status):
    send_status_update_email(complaint, status)
    send_sms_notification(complaint, status)
    send_whatsapp_notification(complaint, status)

    # Admin emergency alert
    if complaint.is_emergency:
        send_whatsapp_notification(complaint, status, emergency=True)

