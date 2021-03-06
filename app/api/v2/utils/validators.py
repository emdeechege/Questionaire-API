import re
# from ....connect import init_db
from app.connect import QuestionerDB


class Validation(QuestionerDB):
    # def __init__(self):
    #     """initialize the user model"""
    #     self.db = init_db()

    """contains validation criteria for authorization"""
    def validate_email(self, email):
        """checks the format of email is standard"""
        expects = "^[\w]+[\d]?@[\w]+\.[\w]+$"
        return re.match(expects, email)


    def validate_password(self, password):
        """check that password contains numbers, special characters and letters. Len >6"""
        expects = "r'(?=(.*[0-9]))((?=.*[A-Za-z0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[$#@]))^.{6,12}$'"
        return re.match(expects, password)

    def validate_phone_number(self, phone_number):
        """ check that phone number is digit """
        phone = "^[0-9]+$"
        return re.match(phone, phone_number)

    def username_exists(self, username):
        """ check username exists"""

        curr = QuestionerDB.conn.cursor()
        query = "SELECT username FROM users WHERE username = '%s'" % (username)
        curr.execute(query)
        curr.fetchone()
        print(curr.fetchone())
        if curr.fetchone() is not None:
            return username

    def email_exists(self, email):
        """ check email exists"""

        # curr = self.db.cursor()
        query = "SELECT email FROM users WHERE email = '%s'" % (email)
        return QuestionerDB.fetch_one(query)
        # curr.execute(query)
        # if curr.fetchone() is not None:
        #     return email
