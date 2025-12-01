import unittest
from datetime import datetime
from app import create_app, db
from app.posts.models import Post
from flask import url_for

class PostsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_list_posts_shows_active_only(self):
        a = Post(title="Active", content="A", category="news", is_active=True, author="a")
        b = Post(title="Inactive", content="B", category="tech", is_active=False, author="b")
        db.session.add_all([a, b])
        db.session.commit()

        resp = self.client.get('/posts/')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_data(as_text=True)
        self.assertIn("Active", data)
        self.assertNotIn("Inactive", data)

    def test_create_post_via_form(self):
        with self.client.session_transaction() as sess:
            sess['user'] = 'testuser'

        resp = self.client.post('/posts/create', data={
            'title': 'FormPost',
            'content': 'Form content',
            'category': 'other',
            'enabled': 'y',
            'publish_date': '',
        }, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn('FormPost', html)

        post = db.session.scalar(db.select(Post).where(Post.title == 'FormPost'))
        self.assertIsNotNone(post)
        self.assertEqual(post.author, 'testuser')
        self.assertTrue(post.is_active)

    def test_detail_view(self):
        p = Post(title="DetailTitle", content="Long content", category="news", is_active=True, author="au")
        db.session.add(p); db.session.commit()

        resp = self.client.get(f'/posts/{p.id}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn("DetailTitle", resp.get_data(as_text=True))
        self.assertIn("Long content", resp.get_data(as_text=True))

    def test_update_post(self):
        p = Post(title="Old", content="Old content", category="other", is_active=True, author="au")
        db.session.add(p); db.session.commit()

        resp = self.client.post(f'/posts/{p.id}/update', data={
            'title': 'NewTitle',
            'content': 'New content',
            'category': 'tech',
            'enabled': 'y'
        }, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn('NewTitle', html)

        post = db.session.scalar(db.select(Post).where(Post.id == p.id))
        self.assertEqual(post.title, 'NewTitle')
        self.assertEqual(post.category, 'tech')

    def test_delete_post(self):
        p = Post(title="ToDelete", content="x", category="other", is_active=True, author="au")
        db.session.add(p); db.session.commit()

        resp_get = self.client.get(f'/posts/{p.id}/delete')
        self.assertEqual(resp_get.status_code, 200)
        self.assertIn("Delete", resp_get.get_data(as_text=True))

        resp = self.client.post(f'/posts/{p.id}/delete', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertNotIn("ToDelete", html)

        post = db.session.scalar(db.select(Post).where(Post.id == p.id))
        self.assertIsNone(post)

    def test_create_without_session_sets_anonymous(self):
        resp = self.client.post('/posts/create', data={
            'title': 'AnonPost',
            'content': 'anon body',
            'category': 'other',
            'enabled': 'y'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        post = db.session.scalar(db.select(Post).where(Post.title == 'AnonPost'))
        self.assertIsNotNone(post)
        self.assertEqual(post.author, 'Anonymous')

if __name__ == '__main__':
    unittest.main()
