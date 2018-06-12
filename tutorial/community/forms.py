from django.forms import ModelForm
from models import *


class Form(ModelForm):
    class Meta:
        model = Article
        fields=['name', 'title' , 'contents', 'url','email']

class UploadForm(ModelForm):
    class Meta:
        model = UploadFile
        fields = ['title' , 'file']
    def __init__(self , *args , **kwargs):
        super(ModelForm , self).__init__(*args, **kwargs)
        self.fields['file'].required = False
