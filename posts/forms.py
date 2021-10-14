from django import forms
from .models import Post
# from e_checkapp.serializers import PpPymntTSerializer
# from .models import pp_path_m

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['cover']