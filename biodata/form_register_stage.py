from django import forms
from .models import StageRegistration

class StageRegistrationForm(forms.ModelForm):
    class Meta:
        model = StageRegistration
        fields = '__all__'
        widgets = {
            'dob': forms.TextInput(attrs={'type': 'text'}),
        }
