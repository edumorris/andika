import unittest
from app.models import User

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(pwd = 'pass123125')
    
    def test_password_setter(self):
        self.assertTrue(self.new_user.pwd is not None)
    
    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.assertTrue(self.new_user.verify_password('pass123125')))