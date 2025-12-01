import unittest
from app import create_app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_products_index(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertIn("Goods", data)

    def test_product_item(self):
        response = self.client.get("/products/item/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertIn("Продукт #1", data)

if __name__ == "__main__":
    unittest.main()
