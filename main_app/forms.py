from django.forms import ModelForm
from .models import Listen

class ListenForm(ModelForm):
    class Meta:
        model = Listen
        fields = ['date', 'timeofday']
        