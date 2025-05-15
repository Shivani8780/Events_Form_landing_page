from django import forms
from .models import CandidateBiodata

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

    birth_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Time Of Birth"
    )

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
            'education_custom',
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

    education_custom = forms.CharField(
        max_length=255,
        required=False,
        label="Education",
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

    dob = forms.DateField(label="Date Of Birth", widget=forms.DateInput(attrs={'type': 'date'}))


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
            'declaration': 'Declaration : ભૂદેવ નેટવર્ક ના સિદ્ધાંતો અને નીતિ-નિયમો પ્રમાણે ,  (૧) હું અને મારો પરિવાર , સામે થી આવતા દરેક ભૂદેવ નો કોલ વિનમ્રતા અને શાંતિ થી લઈશું , તેમને અમારો હા / ના , જે પણ જવાબ હોય તે સરળતા , આદરતા-પૂર્વક અને નિહ-સંકોચ થી ફોન ઉપર બોલીને કે પછી વોટ્સએપ માં લખીને (અન્ય રીતે) જણાવીશું .  (૨) કોલ કરનાર સામે વાળા ભૂદેવ નું અમે અપમાન નહીં કરીયે અને જેમ-તેમ તે ભૂદેવ ને ઉતારી નહિ પાડીયે , તેમની સાથે વ્યવસ્થિત વર્તન કરીશું . (૩) આ સાથેજ , પ્રથમ કોલ  કે મેસેજ કરનાર ભૂદેવ ની પણ તેટલીજ જવાબદારી છે કે તે કોઈ પણ પ્રકાર થી સામે વાળા પાત્ર કે પછી તેમના માતા-પિતા ને વારંવાર ફોન કરીને કે અન્ય રીતે હેરાન નહિ કરે....  જો કોઈ પણ ફેમિલી ની અમોને અમુક ઉમેદવાર-ફેમિલી માટે કમ્પ્લેન મળશે તો તેમનો બાયોડેટા રદ્દ કરવામાં આવશે અને તેમને આગામી લગ્ન-મેળા માં સ્થાન નહિ મળે . ભૂદેવ નો અર્થ છે ભૂ + દેવ , એટલે કે ધરતી પરનો દેવ , તો આપણા ગુણો પણ દેવો જેવા હોવા જોઈએ . શુભ અને શુદ્ધ વિચાર રાખવા જોઈએ , વિચાર થી વૃત્તિ બને છે , વૃત્તિ થી વાણી અને વર્તન નિર્માણ પામે છે , વાણી અને વર્તન થી વ્યક્તિત્વ બને છે અને વ્યક્તિત્વ થીજ માણસ ની ઓળખ થાય છે અને I agree to Terms & Conditions of Bhudev Network organization.',
            'declaration_agree': 'Agree (ઉપર મુજબ હું માનું છું અને તેમ કરીશ) - મારો બાયોડેટા બુકલેટ માં ચોક્કસ સમાવેશ કરશોજી',
            'declaration_disagree': 'Disagree (ઉપર મુજબ હું નહિ માનું)  - મારો બાયોડેટા કેન્સલ કરી દેજો',
            'gender': 'Candidate Gender',
            'registration_by': 'Who is doing this Registration ? (કોણ રેજીસ્ટ્રેશન કરી રહ્યું છે ? એ વિગત અહીં લખશો)   Example : SELF / Candidate\'s Father (Name) / Candidate\'s Mother (Name) /  Candidate\'s Brother (Name)  , etc',
            'registrant_mobile': 'જે આ રેજીસ્ટ્રેશન કરી રહ્યું છે , તે અહીં પોતાનો MOBILE નંબર લખશો // Mention here your own Mobile Number (for Reference & Verification Purpose)',
            'residence_area_category': 'Candidate Current Residence Area Category',
            'current_country': 'Candidate Current Country',
            'visa_status': 'Visa or Residence Status Of Candidate',
            'photograph': 'Upload 1 Candidate Photo (Photo Should be Clear visible front-face, Bright light on Face, No Goggles or Cap , Close-up photo or Passport Size Photo is required)',    

        }
