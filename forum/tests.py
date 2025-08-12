from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

# Create your tests here.

# Set up with user creation
class ForumTests(TestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        # Create a post by user1
        self.post = Post.objects.create(
            author=self.user1,
            title="Test Post",
            body="This is the body of the test post"
        )

    # test 1 forum page loads for logged in user
    def test_forum_page_loads(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum.html')

    # test 2 if logged in user can create posts
    def test_authenticated_user_can_create_post(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('forum'), {
            'title': 'New Post',
            'body': 'New post body text'
        })
        self.assertEqual(Post.objects.count(), 2)
        self.assertRedirects(response, reverse('forum'))

    # test 3 if unlogged in user can create post
    def test_unauthenticated_user_cannot_create_post(self):
        response = self.client.post(reverse('forum'), {
            'title': 'Fail Post',
            'body': 'Should not work'
        })
        self.assertEqual(Post.objects.count(), 1)

    # test 4 if detail page for posts load with logged in user
    def test_post_detail_page_loads(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('post_detail', args=[self.post.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_detail.html')
        self.assertContains(response, self.post.title)

    # test 5 if logged in user can comment on detail page
    def test_authenticated_user_can_comment(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('post_detail', args=[self.post.slug])
        response = self.client.post(url, {
            'body': 'This is a test comment'
        })
        self.assertEqual(Comment.objects.count(), 1)
        self.assertRedirects(response, url)

    # test 6 if unlogged in user can comment
    def test_unauthenticated_user_cannot_comment(self):
        url = reverse('post_detail', args=[self.post.slug])
        response = self.client.post(url, {
            'body': 'Should fail'
        })
        self.assertEqual(Comment.objects.count(), 0)

    # test 7 post like system
    def test_post_like_toggle(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('post_like_toggle', args=[self.post.slug])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes_count, 1)

    # test 8 comment like system
    def test_comment_like_toggle(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            body='Like me!'
        )
        self.client.login(username='user2', password='pass123')
        url = reverse('comment_like_toggle', args=[comment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.likes_count, 1)

    # test 9 if user can edit their own post
    def test_post_edit_by_author(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('post_edit', args=[self.post.slug])
        response = self.client.post(url, {
            'title': 'Edited Title',
            'body': 'Edited body text'
        })
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Edited Title')

    # test 10 if user can edit others posts
    def test_post_edit_by_non_author_forbidden(self):
        self.client.login(username='user2', password='pass123')
        url = reverse('post_edit', args=[self.post.slug])
        response = self.client.post(url, {
            'title': 'Hacked Title',
            'body': 'Hacked text'
        })
        self.assertEqual(response.status_code, 403)

    # test 11 if user can delete their own post
    def test_post_delete_by_author(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('post_delete', args=[self.post.slug])
        # First GET should show confirmation
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        # Then POST should delete
        post_response = self.client.post(url)
        self.assertRedirects(post_response, reverse('forum'))
        self.assertEqual(Post.objects.count(), 0)

    # test 12 if user can delete others posts
    def test_post_delete_by_non_author_forbidden(self):
        self.client.login(username='user2', password='pass123')
        url = reverse('post_delete', args=[self.post.slug])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    # test 13 if user can edit their own comment
    def test_comment_edit_by_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user1, body="Original")
        self.client.login(username='user1', password='pass123')
        url = reverse('comment_edit', args=[self.post.slug, comment.id])
        self.client.post(url, {'body': 'Edited Comment'})
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Edited Comment')

    # test 14 if user can edit others comments
    def test_comment_delete_by_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user1, body="Delete me")
        self.client.login(username='user1', password='pass123')
        url = reverse('comment_delete', args=[self.post.slug, comment.id])
        # Confirmation GET
        self.assertEqual(self.client.get(url).status_code, 200)
        # Actual delete POST
        self.client.post(url)
        self.assertEqual(Comment.objects.count(), 0)

