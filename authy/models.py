from django.db import models
from django.contrib.auth.models import User
from post.models import Post

from django.db.models.signals import post_save
import PIL.Image as Image
from django.conf import settings
import os


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
					profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
					full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

					if os.path.exists(full_path):
						os.remove(full_path)
						
					return profile_pic_name



# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	url = models.CharField(max_length=80, null=True, blank=True)
	profile_info = models.TextField(max_length=150, null=True, blank=True)
	created = models.DateField(auto_now_add=True)
	favorites = models.ManyToManyField(Post)
	picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')

	
	# def save(self, *args, **kwargs):
	# 	super().save()
	# 	img = Image.open(self.picture.path)
	# 	width, height = img.size  # Get dimensions

	# 	if width > 300 and height > 300:
	# 		# keep ratio but shrink down
	# 		img.thumbnail((width, height))

	# 	# check which one is smaller
	# 	if height < width:
	# 		# make square by cutting off equal amounts left and right
	# 		left = (width - height) / 2
	# 		right = (width + height) / 2
	# 		top = 0
	# 		bottom = height
	# 		img = img.crop((left, top, right, bottom))

	# 	elif width < height:
	# 		# make square by cutting off bottom
	# 		left = 0
	# 		right = width
	# 		top = 0
	# 		bottom = width
	# 		img = img.crop((left, top, right, bottom))

	# 	if width > 300 and height > 300:
	# 		img.thumbnail((300, 300))

	# 	img.save(self.picture.path)



	def __str__(self):
		return self.user.username
		

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)