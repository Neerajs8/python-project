import smtplib
import logging
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

class User:
    def __init__(self, user_id, email, phone_number):
        self.user_id = user_id
        self.email = email
        self.phone_number = phone_number

class AccessControlSystem:
    def __init__(self):
        self.authorized_users = {
            'user1': User('user1', 'sanjith50801@gmail.com', '9110225803'),
            'user2': User('user2', 'darshupruthvi007@gmail.com', '0987654321'),
            '123': User('123', 'parkavi.a@msrit.edu', '0987654321'),
             '234': User('234', 'neerajnaidu1718@gmail.com', '0987654321'),
        }

    def is_user_authorized(self, user_id):
        return user_id in self.authorized_users.keys()

    def get_user_info(self, user_id):
        if self.is_user_authorized(user_id):
            user = self.authorized_users[user_id]
            return user.email, user.phone_number
        return None, None

class WiFiProvisioning:
    def __init__(self):
        self.previous_passwords = set()

    def generate_password(self):
        while True:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            if password not in self.previous_passwords:
                self.previous_passwords.add(password)
                return password

    def send_email(self, email, password):
        try:
            sender_email = 'sn0325056@gmail.com'
            receiver_email = email

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "WiFi Password"

            body = f"Dear User,\n\nYour WiFi password is: {password}\n\nRegards,\nYour Building Management Team"
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, "jocb xtco xwfc osln")
                server.sendmail(sender_email, receiver_email, message.as_string())

            logging.info("WiFi password sent to user's email.")
        except Exception as e:
            logging.error(f"Error sending email: {e}")

    def send_sms(self, phone_number, password):
        try:
            account_sid = 'AC2aed22fae95fd082549f774410c2ef1a'
            auth_token = 'f8ed0f2c0ab767009f6b04bf0c52c3a6'

            client = Client(account_sid, auth_token)

            twilio_number = '+919110225803'

            to_number = phone_number

            message_body = "password is " + password

            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=to_number
            )

            logging.info("WiFi password sent to user's phone number.")

        except Exception as e:
            logging.error(f"Error sending SMS: {e}")


def main():
    access_control = AccessControlSystem()
    wifi_provisioning = WiFiProvisioning()

    logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    while True:
        user_id = input("Enter user ID: ")

        if access_control.is_user_authorized(user_id):
            logging.info("User is authorized.")
            email, phone_number = access_control.get_user_info(user_id)
            password = wifi_provisioning.generate_password()
            wifi_provisioning.send_email(email, password)
            wifi_provisioning.send_sms(phone_number, password)
            print("WiFi password sent to user's email and phone number.")
            break
        else:
            logging.warning("User is not authorized.")
            print("User is not authorized. Sending notification to admin...")

            admin_email = "sn0325056@gmail.com"
            admin_phone = "+919110225803"
            admin_message = f"Unauthorized access attempt by user ID: {user_id}"
            wifi_provisioning.send_email(admin_email, admin_message)
            wifi_provisioning.send_sms(admin_phone, admin_message)

            print("Notification sent to admin. Please try again.")

if __name__ == "__main__":
    main()
