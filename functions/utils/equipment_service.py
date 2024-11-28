import os
import asyncio
from jinja2 import Template
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from database.repositories.user_repository import UserDAO

from models.equipment_model import NotificationBody

from dotenv import load_dotenv
load_dotenv('.env')

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME="Indoor Tracking",
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True
)

def load_html(file_path: str, context: str) -> str:
    with open(file_path, 'r') as file:
      template = Template(file.read())
      return template.render(context) 
    
async def send_mail_notification(subject: str, email_to: str, equipment_name: str, register: str, date: datetime, location: str):
    context = {
        "name": equipment_name,
        "register": register,
        "date": date,
        "location": location
    }

    template_path = "utils/templates/email_notification.html"
    html_content = load_html(template_path,context)

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html_content,
        subtype='html',
        attachments=[{
          "file": "utils/assets/logo.png",  # Caminho para a imagem
          "headers": {"Content-ID": "<logo>"}  # Defina o Content-ID para referenciar no HTML
        }]
    )
    fm = FastMail(conf)
    # asyncio.create_task(fm.send_message(message))
    await fm.send_message(message)

async def notify_all_users(notification_body: NotificationBody):
    userDAO = UserDAO()
    emails = userDAO.get_users_emails()
    
    date_brasilia = notification_body.date.astimezone(ZoneInfo("America/Sao_Paulo"))
    date_key = date_brasilia.strftime("%Y-%m-%d %H:%M:%S")
    if emails:
        for email in emails:
            await send_mail_notification('Equipamento mudou de sala', email['email'], notification_body.equipment_name, notification_body.register_, date_key, notification_body.location)