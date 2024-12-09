from django import forms
from post.models import Post


class NewPostForm(forms.ModelForm):
	video = forms.FileField(widget=forms.FileInput(attrs={"id":"file-input","class":"hidden","onchange":"previewVideo()"}),required=True)
	caption = forms.CharField(widget=forms.TextInput(attrs={"class":"w-full border p-2.5 rounded-md focus:outline-none","placeholder":"Eg. Nice fun Video"}), required=True)
	tags = forms.CharField(widget=forms.TextInput(attrs={"class":"w-full border p-2.5 rounded-md focus:outline-none","placeholder":"Eg. fast,music"}), required=True)
	class Meta:
		model = Post
		fields = ('video', 'caption', 'tags')
	


# class PostUpdateForm(forms.ModelForm):
# 	video = forms.FileField(required=True)
# 	caption = forms.CharField(widget=forms.Textarea(attrs={"class":"w-full border p-2.5 rounded-md focus:outline-none"}), required=True)
# 	tags = forms.CharField(widget=forms.TextInput(attrs={"class":"w-full border p-2.5 rounded-md focus:outline-none"}), required=True)
# 	class Meta:
# 		model = Post
# 		fields = ('video', 'caption', 'tags')



class PostUpdateForm(forms.ModelForm):
	video = forms.FileField(widget=forms.FileInput(attrs={"id":"file-input","class":"hidden","onchange":"previewVideo()"}),required=True)
	caption = forms.CharField(
		widget=forms.TextInput(attrs={"class": "w-full border p-2.5 rounded-md focus:outline-none"}),
		required=True,
	)
	tags = forms.CharField(
		widget=forms.TextInput(attrs={"class": "w-full border p-2.5 rounded-md focus:outline-none"}),
		required=True,
	)

	class Meta:
		model = Post
		fields = ('video', 'caption', 'tags')    
"""

class NewPostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('picture', 'caption', 'tags')
		def __init__(self, *args, **kwargs):
			super(NewPostForm, self).__init__(*args, **kwargs)
			self.fields['caption'].widget.attrs['placeholder'] = 'Add a Title'
			self.fields['tags'].widget.attrs['placeholder'] = 'Tell everyone what your pin is about..'
			
			for visible in self.visible_fields():
				if visible.name == 'description':
					visible.field.widget.attrs['class'] = 'description-input border form-control'
				elif visible.name == 'board':
					visible.field.widget.attrs['class'] = 'board-input border form-control'
				else:
					visible.field.widget.attrs['class'] = 'form-control border rounded-pill'

"""