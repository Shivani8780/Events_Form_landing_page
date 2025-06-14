from django import forms
from .models import CandidateBiodata
from django.core.exceptions import ValidationError
from .validators import validate_not_mpo
from django.core.exceptions import ValidationError
from .validators import validate_not_mpo


class CandidateBiodataForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    RESIDENCE_AREA_CATEGORY_CHOICES = [
        ('Gujarat Region (North , Central , South)', 'Gujarat Region (North , Central , South)'),
        ('Saurshtra - Kachchh Region', 'Saurshtra - Kachchh Region'),
        ('Mumbai - Maharashtra - Rest of India Region', 'Mumbai - Maharashtra - Rest of India Region'),
        ('NRI (Non Residential Indian - Any Visa) Region (Out of India)', 'NRI (Non Residential Indian - Any Visa) Region (Out of India)'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, label="Candidate Gender")
    registration_by = forms.CharField(max_length=255, required=True, label="Who is doing this Registration ? (કોણ રેજીસ્ટ્રેશન કરી રહ્યું છે ? એ વિગત અહીં લખશો)   🔴 Example : SELF / Candidate's Father (Name) / Candidate's Mother (Name) /  Candidate's Brother (Name)  , etc 🔴")
    registrant_mobile = forms.CharField(max_length=20, required=True, label="જે આ રેજીસ્ટ્રેશન કરી રહ્યું છે , તે અહીં પોતાનો MOBILE નંબર લખશો // Mention here your own Mobile Number (for Reference & Verification Purpose)")
    candidate_current_city = forms.CharField(max_length=255, required=False, label="Candidate Current City / ઉમેદવાર પોતે હાલ કાયા CITY / શહેર / ગામ માં રહે છે , તે અહીં લખો :")
    residence_area_category = forms.ChoiceField(choices=RESIDENCE_AREA_CATEGORY_CHOICES, required=True, label="Candidate Current Residence Area Category")
    current_country = forms.CharField(max_length=255, required=True, label="Candidate Current Country")

    visa_status = forms.ChoiceField(choices=CandidateBiodata.VISA_STATUS_CHOICES, required=True, label="Visa or Residence Status Of Candidate")
    marital_status = forms.ChoiceField(choices=CandidateBiodata.MARITAL_STATUS_CHOICES, required=True, label="Marriage Status")
    shani_mangal = forms.ChoiceField(choices=CandidateBiodata.SHANI_MANGAL_CHOICES, required=False, label="Shani / Mangal", initial='')

    birth_time = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'text'}),
        label="Time Of Birth"
    )
    dob = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'text'}),
        label="Date Of Birth"
    )

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        # Accept any text, no validation
        return dob

    def clean_birth_time(self):
        birth_time = self.cleaned_data.get('birth_time')
        # Accept any text, no validation
        return birth_time

    def clean(self):
        cleaned_data = super().clean()
        # Override dob and birth_time to bypass model validation
        dob_raw = self.data.get('dob')
        birth_time_raw = self.data.get('birth_time')
        if dob_raw is not None:
            cleaned_data['dob'] = dob_raw
        if birth_time_raw is not None:
            cleaned_data['birth_time'] = birth_time_raw
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Assign raw text values to model fields to bypass validation errors
        dob_raw = self.cleaned_data.get('dob')
        birth_time_raw = self.cleaned_data.get('birth_time')
        if dob_raw is not None:
            instance.dob = dob_raw
        if birth_time_raw is not None:
            instance.birth_time = birth_time_raw
        if commit:
            instance.save()
        return instance
    monthly_income = forms.CharField(
        required=False,
        label="Salary (optional) Per Month Salary)"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required except monthly_income
        for field_name, field in self.fields.items():
            if field_name != 'monthly_income':
                field.required = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reorder fields to place candidate_current_city before residence_area_category and current_country
        field_order = [
            'candidate_name',
            'gender',
            'registration_by',
            'registrant_mobile',
            'candidate_current_city',
            'residence_area_category',
            'current_country',
            'visa_status',
            'photograph',
            'dob',
            'birth_time',
            'birth_place',
            'height',
            'weight',
            'education',
            'education_details',
            'occupation',
            'occupation_details',
            'monthly_income',
            'marital_status',
            'nadi',
            'shani_mangal',
            'type_of_brahmin',
            'gotra',
            'kuldevi',
            'father_name',
            'father_mobile',
            'mother_name',
            'mother_mobile',
            'siblings',
            'partner_education',
            'partner_location',
            'partner_age_bracket',
            'other_specific_choice',
            'declaration',
            'declaration_agree',
            'declaration_disagree',
        ]
        self.order_fields(field_order)

    OCCUPATION_CHOICES = [
        ('Government Job', 'Government Job'),
        ('Private MNC Job', 'Private MNC Job'),
        ('Job', 'Job'),
        ('Self Employed (Own Practice)', 'Self Employed (Own Practice)'),
        ('Own Business', 'Own Business'),
        ('Job + Business', 'Job + Business'),
        ('Free Lancing', 'Free Lancing'),
        ('Student (Studies Running)', 'Student (Studies Running)'),
        ('Searching Job', 'Searching Job'),
        ('Home Works (ghar-kaam)', 'Home Works (ghar-kaam)'),
    ]
    occupation = forms.ChoiceField(choices=OCCUPATION_CHOICES, required=True, label="Job/Business/Occupation Category")

    occupation_details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control small-input', 'style': 'height: 60px;'}),
        required=False,
        label="Details on Job / Business / Occupation",
    )


    height = forms.CharField(
        max_length=50,
        required=False,
        label="Height (In Feet)",
        help_text='Example: Enter height like 4.05 feet for 4 feet 5 inches.'
    )

    partner_age_bracket = forms.CharField(
        max_length=100,
        required=False,
        label="પાર્ટનર ઉંમર શ્રેણી (Partner Age Bracket)",
        help_text='Example: Enter age range like 27 to 30.'
    )

#    dob = forms.DateField(label="Date Of Birth", widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = CandidateBiodata
        fields = '__all__'
        widgets = {
            # Removed fields widgets
        }
        labels = {
            'candidate_name': 'Name Of Candidate / ઉમેદવાર નું નામ',
            'dob': 'Date Of Birth',
            'birth_time': 'Time Of Birth',
            'birth_place': 'Birth Place',
            'height': 'Height (In Feet)',
            'weight': 'Weight (In KG)',
            'education': 'Highest Education Category',
            'education_details': 'Education',
            'occupation': 'Job/Business/Occupation Category',
            'occupation_details': 'Details on Job / Business / Occupation',
            'monthly_income': 'Salary (optional) Per Month Salary)',
            'partner_education': 'Choice Of Education (Partner Preference)',
            'partner_location': 'Choice Of Location (Partner Preference)',
            'partner_age_bracket': 'Choice Of Age Gap/ Difference in Year (Partner Preference)',
            'declaration': 'Declaration : હું અહીં ખાત્રી આપુ છું કે, મે ભરેલી, ઉપરોક્ત બધી માહિતી ખરી છે. સાચી છે, અને મે બધી માહિતી ચેક કરી લીધી છે. મારો બાયોડેટા લેટેસ્ટ બુકલેટ મા સમાવેશ કરશો. (I hereby declare that all above info filled by myself is correct & all right and i have checked all info before submission of this Form. Please include my Biodata in latest Biodata Booklet)',
            'declaration_agree': 'Agree (ઉપર મુજબ હું માનું છું અને તેમ કરીશ) - મારો બાયોડેટા બુકલેટ માં ચોક્કસ સમાવેશ કરશોજી',
            'declaration_disagree': 'Disagree (ઉપર મુજબ હું નહિ માનું)  - મારો બાયોડેટા કેન્સલ કરી દેજો',
        'gender': 'Candidate Gender',
        'registration_by': 'Who is doing this Registration ? (કોણ રેજીસ્ટ્રેશન કરી રહ્યું છે ? એ વિગત અહીં લખશો)   Example : SELF / Candidate\'s Father (Name) / Candidate\'s Mother (Name) /  Candidate\'s Brother (Name)  , etc',
        'registrant_mobile': 'જે આ રેજીસ્ટ્રેશન કરી રહ્યું છે , તે અહીં પોતાનો MOBILE નંબર લખશો // Mention here your own Mobile Number (for Reference & Verification Purpose)',
        'residence_area_category': 'Candidate Current Residence Area Category',
        'current_country': 'Candidate Current Country',
        'visa_status': 'Visa or Residence Status Of Candidate',
        'photograph': 'Upload 1 Candidate Photo (Photo Should be Clear visible front-face, Bright light on Face, No Goggles or Cap , Close-up photo or Passport Size Photo is required)',
        'mother_mobile': "Mother's Whatsapp Number",
        'father_mobile': "Father's Whatsapp Number",
        'whatsapp_number': "Whatsapp Number (For verification)",
        'kuldevi': 'Any Disability/ Details',

        }
