import unittest
from app import create_app, db
from app.users.models import User
from sqlalchemy import select

class AuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("test") 
        cls.app.config.update({
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        })
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        pass

    def tearDown(self):
        with self.app.app_context():
            db.session.rollback()
            db.session.query(User).delete()
            db.session.commit()

    def test_register_page_loads(self):
        resp = self.client.get("/auth/register")
        self.assertEqual(resp.status_code, 200)
        text = resp.get_data(as_text=True)
        self.assertTrue("Реєстрація" in text or "Register" in text)

    def test_login_page_loads(self):
        resp = self.client.get("/auth/login")
        self.assertEqual(resp.status_code, 200)
        text = resp.get_data(as_text=True)
        self.assertTrue("Вхід" in text or "Login" in text)

    def test_registration_creates_user(self):
        data = {
            "username": "unittest",
            "email": "unittest@example.com",
            "password": "strongpass",
            "password2": "strongpass",
        }
        resp = self.client.post("/auth/register", data=data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        with self.app.app_context():
            user = db.session.scalar(select(User).where(User.username == "unittest"))
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "unittest@example.com")
            self.assertTrue(user.check_password("strongpass"))

    def test_login_and_logout_flow(self):
        with self.app.app_context():
            u = User(username="alice_unittest", email="alice_ut@example.com")
            u.set_password("secret123")
            db.session.add(u)
            db.session.commit()

        login_data = {"username": "alice_unittest", "password": "secret123", "remember": "y"}
        resp = self.client.post("/auth/login", data=login_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        text = resp.get_data(as_text=True)
        self.assertIn("alice_unittest", text)

        resp2 = self.client.get("/auth/profile")
        self.assertEqual(resp2.status_code, 200)
        text2 = resp2.get_data(as_text=True)
        self.assertIn("alice_unittest", text2)

        resp3 = self.client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(resp3.status_code, 200)

        resp4 = self.client.get("/auth/profile", follow_redirects=False)
        self.assertIn(resp4.status_code, (302, 303))
        location = resp4.headers.get("Location", "")
        self.assertIn("/auth/login", location)


if __name__ == "__main__":
    unittest.main(verbosity=2)
