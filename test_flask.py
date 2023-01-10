from unittest import TestCase

from app import app
from models import db, User, Post, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """ Tests Views for User Model """

    def setUp(self):
        """ Add sample pet """

        User.query.delete()

        user = User(first_name="Billy", last_name="Bob")
        db.session.add(user)
        db.session.flush()
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """ Clean up any fouled transactions """

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Billy Bob', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Billy Bob', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post("/users/new",
                               data={"firstName": "New", "lastName": "User"})

            user = User.query.filter_by(last_name="User").first()

            self.assertEqual(user.first_name, "New")

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete')
            user = User.query.get(self.user_id)

            self.assertFalse(user)


class PostViewsTestCase(TestCase):
    """ Test Views for Post Model """

    def setUp(self):
        """ Add sample post """

        Post.query.delete()
        User.query.delete()

        post = Post(title="Test Post", content="Content")
        user = User(first_name='Test', last_name='User')
        db.session.add(post)
        db.session.add(user)
        db.session.flush()
        db.session.commit()

        self.post_id = post.id
        self.user_id = user.id

    def tearDown(self):
        """ Clean up any fouled transactions """

        db.session.rollback()

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)

    def test_create_post(self):
        """ Tests Creating a Post """

        with app.test_client() as client:
            resp = client.post(f'users/{self.user_id}/posts/new',
                               data={'title': 'New Post', 'content': 'New Content'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            post = Post.query.filter_by(content='New Content').first()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(post.title, 'New Post')

    def test_edit_post(self):
        """ Tests Editing a Post """

        with app.test_client() as client:
            resp = client.post(
                f'/posts/{self.post_id}/edit', data={'title': 'Edited Post', 'content': 'Edited Content'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edited Post', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete')
            post = Post.query.get(self.post_id)

            self.assertFalse(post)


class TagViewsTestCase(TestCase):
    """ Test Views for Tag Model """

    def setUp(self):
        """ Creates Test Tag """

        Tag.query.delete()

        tag = Tag(name='Test')
        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

    def tearDown(self):
        """ Cleans up any unwanted transactions """

        db.session.rollback()

    def test_show_tags(self):
        """ Tests Tag List Route """

        with app.test_client() as client:
            resp = client.get('/tags')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_tag(self):
        """ Tests Showing Individual Tag """

        with app.test_client() as client:
            resp = client.get(f'tags/{self.tag_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_create_tag(self):
        """ Tests Creating a New Tag """

        with app.test_client() as client:
            resp = client.post(
                f'/tags/new', data={'tag-name': 'New Tag'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Tag', html)

    def test_edit_tag(self):
        """ Tests Editing a Tag """

        with app.test_client() as client:
            resp = client.post(
                f'/tags/{self.tag_id}/edit', data={'tag-name': 'Edited Tag'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edited Tag', html)

    def test_delete_tag(self):
        """ Tests Deleting a Tag """

        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag_id}/delete')

        tag = Tag.query.get(self.tag_id)

        self.assertFalse(tag)
