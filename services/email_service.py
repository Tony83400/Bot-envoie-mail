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
    
    with app_context.app_context():
        pending_apps = Application.query.filter_by(status='En attente').all()

        for app in pending_apps:
            # Création manuelle de la date au format IMAP (DD-Mon-YYYY en anglais) pour éviter les erreurs de locale
            months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
            date_str = f"{app.date_sent.day:02d}-{months[app.date_sent.month]}-{app.date_sent.year}"
            
            # Recherche des mails depuis la date d'envoi
            status, data = mail.search(None, f'FROM "{app.contact_email}" SINCE {date_str}')
            
            if status == 'OK' and data[0]:
                mail_ids = data[0].split()
                
                # On vérifie les mails trouvés en partant du plus récent
                for email_id in reversed(mail_ids):
                    res, msg_data = mail.fetch(email_id, '(RFC822)')
                    if res == 'OK':
                        raw_email = msg_data[0][1]
                        import email
                        from email.utils import parsedate_to_datetime
                        from datetime import timezone
                        
                        msg = email.message_from_bytes(raw_email)
                        
                        if 'Date' in msg:
                            msg_date = parsedate_to_datetime(msg['Date'])
                            # Convertir la date du mail en UTC Naive pour la comparer à la BDD
                            msg_date_utc = msg_date.astimezone(timezone.utc).replace(tzinfo=None)
                            
                            # Si le mail a bien été reçu STRICTEMENT APRES l'envoi de la candidature
                            if msg_date_utc > app.date_sent:
                                body = ""
                                if msg.is_multipart():
                                    for part in msg.walk():
                                        if part.get_content_type() == "text/plain":
                                            payload = part.get_payload(decode=True)
                                            if payload:
                                                body = payload.decode(errors='ignore')
                                            break
                                else:
                                    payload = msg.get_payload(decode=True)
                                    if payload:
                                        body = payload.decode(errors='ignore')
                                
                                # Stocker l'extrait
                                app.reply_body = body[:1000].strip() if body else "Pas de texte détecté."
                                app.status = 'Répondu'
                                replied_count += 1
                                break # On arrête la recherche pour cette candidature car on a trouvé la réponse
                
        if replied_count > 0:
            db.session.commit()

    mail.logout()
    return replied_count
