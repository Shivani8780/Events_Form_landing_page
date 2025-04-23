from django import forms
from .models import CandidateBiodata

class CandidateBiodataForm(forms.ModelForm):
    class Meta:
        model = CandidateBiodata
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'birth_time': forms.TimeInput(attrs={'type': 'time'}),
            'alcoholic_drinks': forms.CheckboxInput(),
            'smoke': forms.CheckboxInput(),
            'legal_police_case': forms.CheckboxInput(),
        }
