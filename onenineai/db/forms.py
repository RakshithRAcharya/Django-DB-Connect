from django.forms import ModelForm
from .models import DB

class DBForm(ModelForm):
    class Meta:
        model = DB
        fields = '__all__'