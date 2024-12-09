from django.db import models
from post.models import Post
from django.contrib.auth.models import User 
from notifications.models import Notification

from django.db.models.signals import post_save, post_delete

# Create your models here.

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	
	def user_comment_post(sender, instance, *args, **kwargs):
		comment = instance
		post = comment.post
		text_preview = comment.body[:90]
		sender = comment.user
		notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview ,notification_type=2)
		notify.save()

	def user_del_comment_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=2)
		notify.delete()


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_replies')
    body = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.owner.username}\'s reply to "{self.comment.body[:15]}..." comment: {self.body[:15]}...'

class CommentLikes(models.Model):
		user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_like')
		comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')

		def user_liked_post(sender, instance, *args, **kwargs):
			like = instance
			comment = like.comment
			sender = like.user
			notify = Notification(comment=comment, sender=sender, user=comment.user, notification_type=1)
			notify.save()

		def user_unlike_post(sender, instance, *args, **kwargs):
			like = instance
			comment = like.comment
			sender = like.user

			notify = Notification.objects.filter(comment=comment, sender=sender, notification_type=1)
			notify.delete()

#Comment
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)

#Likes
post_save.connect(CommentLikes.user_liked_post, sender=CommentLikes)
post_delete.connect(CommentLikes.user_unlike_post, sender=CommentLikes)