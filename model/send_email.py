# Gmail Sender with Debug

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_gmail(sender_email, app_password, receiver_email, subject, body):
    # Gmail SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Create server object with debug level (1)
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # This will show detailed debug output
        
        # Start the connection
        print("Starting connection to server...")
        server.ehlo()
        
        # Start TLS
        print("Starting TLS encryption...")
        server.starttls()
        
        # Login
        print("Attempting to log in...")
        server.login(sender_email, app_password)
        
        # Send email
        print("Sending email...")
        server.send_message(message)
        
        print("Email sent successfully!")
        
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication failed! Common causes:")
        print("1. You're not using an App Password (required for Gmail)")
        print("2. App Password is incorrect")
        print("3. Less secure app access is not enabled (if not using App Password)")
        print(f"Error details: {str(e)}")
        
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {str(e)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        try:
            server.quit()
        except:
            pass

# Example usage
if __name__ == "__main__":
    # Your Gmail credentials
    sender_email = "kushalmandala29@gmail.com"  # Your Gmail address
    app_password = "znny kcpa xnhk nqvp"  # Your App Password (not your regular Gmail password)
    receiver_email = "6305513406s@gmail.com"
    
    subject = "Test Email"
    body = "This is a test email sent from Python."
    
    send_gmail(sender_email, app_password, receiver_email, subject, body)