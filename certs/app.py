import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os

def create_certificate(name, output_path):
    # Open the certificate template
    template = Image.open('certificate.jpg')
    
    # Create a copy to draw on
    certificate = template.copy()
    draw = ImageDraw.Draw(certificate)
    
    # Load a font (you'll need to specify the path to your font file)
    font_size = 60
    font = ImageFont.truetype('Arial.ttf', font_size)
    
    # Get the size of the text using textbbox instead of textsize
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position to center the text
    x = (certificate.width - text_width) / 2
    y = (certificate.height - text_height) / 2
    
    # Add the name to the certificate
    draw.text((x, y), name, fill='black', font=font)
    
    # Save the certificate
    certificate.save(output_path)

def send_certificate(email, certificate_path, sender_email, sender_password):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Your Certificate'
    
    # Add body text
    body = "Please find your certificate attached."
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the certificate
    with open(certificate_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename="certificate.jpg")
        msg.attach(img)
    
    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

def main():
    # Email credentials
    sender_email = "3beeral9afran@gmail.com"
    sender_password = "xxxx xxxx xxxx xxxx"  # Use App Password for Gmail
    
    # Read the CSV file
    df = pd.read_csv('participants.csv')
    
    # Process each participant
    for index, row in df.iterrows():
        name = row['Name']
        email = row['Email']
        
        # Create certificate
        certificate_path = name+'certificate.png'
        os.makedirs('certificates', exist_ok=True)
        create_certificate(name, certificate_path)
        
        # Send certificate
        try:
            send_certificate(email, certificate_path, sender_email, sender_password)
            print("Certificate sent successfully to "+name)
        except Exception as e:
            print("Error sending certificate to "+name)

if __name__ == "__main__":
    main()
