from django import forms
from comment.models import Comment

class CommentForm(forms.ModelForm):
	body = forms.CharField(widget=forms.TextInput(attrs={"class":"bg-[#F1F1F2] text-[14px] focus:outline-none w-full lg:max-w-[420px] p-2 rounded-lg","placeholder":"Give a Comment ..."}), required=True)

	class Meta:
		model = Comment
		fields = ('body',)