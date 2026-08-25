import os
import smtplib
import imaplib
from email.message import EmailMessage
from models import db, Application

def send_application_email(to_email, subject, body, attachment_paths):
    """Envoie un email avec pièces jointes via SMTP Gmail."""
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    if not sender_email or not password:
        raise Exception("Les identifiants email ne sont pas configurés dans le fichier .env")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(body)

    # Ajout des pièces jointes
    for path in attachment_paths:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(path)
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    # Envoi
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

def check_for_replies(app_context):
    """Se connecte en IMAP et vérifie les réponses pour les candidatures en attente."""
    imap_server = "imap.gmail.com"
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not sender_email or not password:
        return 0

    mail = imaplib.IMAP4_SSL(imap_server)
    try:
        mail.login(sender_email, password)
        mail.select('inbox')
    except Exception as e:
        print(f"Erreur de connexion IMAP: {e}")
        return 0
        
    replied_count = 0
    
    with app_context:
        pending_apps = Application.query.filter_by(status='En attente').all()

        for app in pending_apps:
            # Cherche les emails venant du contact
            status, data = mail.search(None, f'FROM "{app.contact_email}"')
            if status == 'OK' and data[0]:
                app.status = 'Répondu'
                replied_count += 1
                
        if replied_count > 0:
            db.session.commit()

    mail.logout()
    return replied_count
