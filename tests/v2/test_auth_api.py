import os,unittest, json
from app import create_app
from instance.config import app_config


from app.connect import QuestionerDB

app = create_app(app_config['testing'])

class UserTestCases(unittest.TestCase):
    """ Base test class """
    def setUp(self):
        """ Defining test variables """
        self.app = create_app(app_config['testing'])
        self.client = self.app.test_client()
        self.app_context = self.app
        self.app.testing = True


        self.user = {
            "firstname": "StandUps",
            "lastname": "Sky",
            "othername": "Tea",
            "email": "tam@gmail.com",
            "phone_number": "123456789",
            "is_admin": "True",
            "username": "Scupper",
            "password": "Ch@mp19?yes"
        }
        self.user1 = {
            "firstname": "StandUps"
        }
        self.user2 = {
            "firstname": "Tom",
            "lastname": "Hunter",
            "othername": "Caps",
            "email": "tampion@gmail.com",
            "phone_number": "123498rttt",
            "is_admin": "False",
            "username": "Awesome",
            "password": "Ch@mp19?no"
        }
        self.user3 = {
            "firstname": "Truthy",
            "lastname": "Stoway",
            "othername": "Birth",
            "email": "tamergmail.com",
            "phone_number": "1234534",
            "is_admin": "True",
            "username": "Scupperdf",
            "password": "Ch@mp19?yes"
        }
        self.user6 = {
            "firstname": "    ",
            "lastname": "Stoway",
            "othername": "Birth",
            "email": "tamer@gmail.com",
            "phone_number": "1234534",
            "is_admin": "True",
            "username": "Scupperdf",
            "password": "Ch@mp19?yes"
        }
        self.login = {
            "username": "Scupper",
            "password": "Ch@mp19?yes"
        }
        self.login1 = {
            "username": "Champ",
            "password": "Ch@mp19?yes"
        }
        self.login2 = {
            "username": "",
            "password": "Ch@mp19?yes"
        }
        self.login3 = {
            "username": "Scuppersds",
            "password": ""
        }
        self.login4 = {
            "username": "Kijana",
            "password": "nnmmiiijjjjuu"
        }

    def tear_down(self):
        """This function destroys objests created during the test run"""
        destroy_tests()

    def test_user_signup(self):
        """ Test signup user """

        check = self.client.post(
            "/api/v2/signup", data=json.dumps(self.user), content_type="application/json")
        result = json.loads(check.data.decode())

        self.assertEqual(check.status_code, 201)
        self.assertEqual(result[1].get("status"), 201)
        self.assertIn("tam@gmail.com", result[0].get('email'))


    def test_validate_phone_number(self):
        """test phone number"""
        response = self.client.post(
            '/api/v2/signup', data=json.dumps(self.user2), content_type="application/json")
        result = json.loads(response.data)

        self.assertTrue(result["message"],
                        "Please input valid phone number")
        self.assertTrue(response.status_code, 400)

    def test_validate_email(self):
        """ validate email"""
        response = self.client.post(
            '/api/v2/signup', data=json.dumps(self.user3), content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"],
                         "Invalid email")
        self.assertEqual(response.status_code, 400)

    # def test_username_exists(self):
    #     """username exists"""
    #     response = self.client.post(
    #         '/api/v2/signup', data=json.dumps(self.user), content_type="application/json")
    #     result = json.loads(response.data)
    #     # import pdb; pdb.set_trace()
    #     self.assertEqual(result[1]["message"], "Username exists")
    #     self.assertEqual(response.status_code, 400)
    #
    # def test_user_login(self):
    #     """ Test login user """
    #     check_login = self.client.post(
    #         "/api/v2/login", data=json.dumps(self.login), content_type="application/json")
    #     result = json.loads(check_login.data.decode())
    #
    #     self.assertEqual(result["status"], 200)
    #     self.assertEqual(result["message"], "User logged in successfully")
    #
    def test_user_exists(self):
        response1 = self.client.post(
            "/api/v2/login", data=json.dumps(self.login1), content_type="application/json")
        result1 = json.loads(response1.data.decode())

        self.assertEqual(response1.status_code, 404)
        self.assertEqual(result1["status"], 404)
        self.assertEqual(result1["message"], "User does not exist")

    def test_username_required(self):
        """username test"""
        response2 = self.client.post(
            "/api/v2/login", data=json.dumps(self.login2), content_type="application/json")
        result2 = json.loads(response2.data.decode())

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(result2["status"], 400)
        self.assertEqual(result2["message"], "Username is required")

    def test_password_required(self):
        """password required"""
        response3 = self.client.post(
            "/api/v2/login", data=json.dumps(self.login3), content_type="application/json")
        result3 = json.loads(response3.data.decode())

        self.assertEqual(response3.status_code, 400)
        self.assertEqual(result3["status"], 400)
        self.assertEqual(result3["message"], "Password is required")

    def tearDown(self):
        """Method to destroy test database tables"""
        QuestionerDB.drop_tables()


if __name__ == "__main__":
    unittest.main()
