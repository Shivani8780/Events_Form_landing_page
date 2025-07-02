from django.db import models
from django.db import models

class CandidateBiodata(models.Model):
    # Personal Details
    candidate_name = models.CharField(max_length=255)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    registration_by = models.CharField(max_length=255, blank=True, null=True)
    registrant_mobile = models.CharField(max_length=20, unique=True)
    candidate_current_city = models.CharField(max_length=255, blank=False, null=False)
    dob = models.CharField(max_length=50, blank=True, null=True)
    MARITAL_STATUS_CHOICES = [
        ('Never Married', 'Never Married'),
        ('One Time Gol-Dhana But then Cancel', 'One Time Gol-Dhana But then Cancel'),
        ('One Time Engagement (Vivah) but afterwards cancel', 'One Time Engagement (Vivah) but afterwards cancel'),
        ('Divorce', 'Divorce'),
        ('Widow', 'Widow'),
    ]
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS_CHOICES, default='Never Married')
    DISABILITY_CHOICES = [
        ('No', 'No'),
        ('Yes', 'Yes'),
        ('Minor Problem', 'Minor Problem'),
    ]
    birth_time = models.CharField(max_length=50, blank=True, null=True)
    birth_place = models.CharField(max_length=255)
    RESIDENCE_AREA_CATEGORY_CHOICES = [
        ('Gujarat Region (North , Central , South)', 'Gujarat Region (North , Central , South)'),
        ('Saurshtra - Kachchh Region', 'Saurshtra - Kachchh Region'),
        ('Mumbai - Maharashtra - Rest of India Region', 'Mumbai - Maharashtra - Rest of India Region'),
        ('NRI (Non Residential Indian - Any Visa) Region (Out of India)', 'NRI (Non Residential Indian - Any Visa) Region (Out of India)'),
    ]
    residence_area_category = models.CharField(max_length=100, choices=RESIDENCE_AREA_CATEGORY_CHOICES, blank=True, null=True)
    current_country = models.CharField(max_length=255, blank=True, null=True)
    VISA_STATUS_CHOICES = [
        ('Indian Citizen', 'Indian Citizen'),
        ('NRI - Student Visa', 'NRI - Student Visa'),
        ('NRI - Work Permit', 'NRI - Work Permit'),
        ('NRI - PR', 'NRI - PR'),
        ('NRI - PR In Process', 'NRI - PR In Process'),
        ('NRI - Green Card (USA)', 'NRI - Green Card (USA)'),
        ('NRI - Blue Card (EU)', 'NRI - Blue Card (EU)'),
        ('NRI - Citizenship', 'NRI - Citizenship'),
        ('NRI - Visitor Visa', 'NRI - Visitor Visa'),
        ('NRI - H1B (USA)', 'NRI - H1B (USA)'),
    ]
    visa_status = models.CharField(max_length=30, choices=VISA_STATUS_CHOICES, default='Indian Citizen')
    visa_status_details = models.CharField(max_length=255, blank=True, null=True, editable=False)
    height = models.CharField(max_length=50, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)
    EDUCATION_CHOICES = [
        ('Undergraduate', 'Undergraduate (10th 12th Pass / Fail , Diploma , ITI , Not Completed Graduation)'),
        ('Graduate', 'Graduate (BA , B.Com. , B.Sc. , BE , BTech, LLB , B. Arch., BBA , BCA etc)'),
        ('Masters', 'Masters (MA , MCom., MSc., ME , MTech, M.Arch , M.Phil, etc Masters Degree holders)'),
        ('CA_CS_ICWA_CPA_ACCA_CIMA', 'CA , CS , ICWA , CPA , ACCA , CIMA , etc'),
        ('Doctor', 'Doctor - Medical - Pharmacy - Dentist - Physiotherapist - Paramedical - Nursing'),
        ('PhD_UPSC_GPSC', 'PhD , UPSC , GPSC (IAS , IPS, etc) , Mayor , Civil Services etc'),
        ('Other', 'Any Other Education Category'),
    ]
    education = models.CharField(max_length=255, choices=EDUCATION_CHOICES)
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
    occupation = models.CharField(max_length=255, choices=OCCUPATION_CHOICES)
    occupation_details = models.TextField(blank=True, null=True)
    monthly_income = models.CharField(max_length=100, blank=True, null=True)
    SHANI_MANGAL_CHOICES = [
        ('Yes ( Nirdosh )', 'Yes ( Nirdosh )'),
        ('Yes ( Heavy)', 'Yes ( Heavy)'),
        ('No', 'No'),
        ("Don't Know", "Don't Know"),
        ("Dont't Believe", "Dont't Believe"),
    ]
    shani_mangal = models.CharField(max_length=20, choices=SHANI_MANGAL_CHOICES, blank=True, null=True)

    NADI_CHOICES = [
        ('Aadhya', 'Aadhya'),
        ('Madhya', 'Madhya'),
        ('Antya', 'Antya'),
        ("I Dont Know", "I Dont Know"),
        ("We Dont Believe", "We Dont Believe"),
    ]
    nadi = models.CharField(max_length=20, choices=NADI_CHOICES, blank=True, null=True)

    # Contact Details
    email = models.EmailField(max_length=254, blank=False, null=False)
    whatsapp_number = models.CharField(max_length=20, blank=False, null=False)

    # Family Details
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    father_mobile = models.CharField(max_length=20)
    mother_mobile = models.CharField(max_length=20)
    type_of_brahmin = models.CharField(max_length=255, blank=True, null=True)
    gotra = models.CharField(max_length=255, blank=True, null=True)
    kuldevi = models.CharField(max_length=255, blank=True, null=True)
    siblings = models.CharField(max_length=255, blank=True, null=True)

    # Partner Preferences
    partner_location = models.CharField(max_length=255, blank=True, null=True)
    partner_age_bracket = models.CharField(max_length=100, blank=True, null=True)
    partner_education = models.CharField(max_length=255, blank=True, null=True)
    other_specific_choice = models.TextField(blank=True, null=True)

    # Photograph - use standard ImageField for local storage
    photograph = models.ImageField(upload_to='photographs/')

    submitted_at = models.DateTimeField(auto_now_add=True)

    DECLARATION_CHOICES = [
        ('Agree', 'Agree (ઉપર મુજબ હું માનું છું અને તેમ કરીશ) - મારો બાયોડેટા બુકલેટ માં ચોક્કસ સમાવેશ કરશોજી'),
        ('Disagree', 'Disagree (ઉપર મુજબ હું નહિ માનું)  - મારો બાયોડેટા કેન્સલ કરી દેજો'),
    ]
    declaration = models.CharField(max_length=20, choices=DECLARATION_CHOICES, blank=True, null=True)
    education_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.candidate_name

class GalleryImage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='gallery_images/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"

class AdvancePassBooking(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField()
    entry_token_quantity = models.PositiveIntegerField(default=0)
    tea_coffee_quantity = models.PositiveIntegerField(default=0)
    unlimited_buffet_quantity = models.PositiveIntegerField(default=0)
    payment_screenshot = models.ImageField(
        upload_to='payment_screenshots/',
        storage=RawMediaCloudinaryStorage()
    )
    created_at = models.DateTimeField(auto_now_add=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} - Entry Token: {self.entry_token_quantity}, Tea-Coffee: {self.tea_coffee_quantity}, Buffet: {self.unlimited_buffet_quantity}"

class AdvanceBookletBooking(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField()
    with_courier = models.BooleanField(default=True)
    girls_booklet_with = models.BooleanField(default=False)
    boys_booklet_with = models.BooleanField(default=False)
    courier_address = models.TextField(blank=True, null=True)
    payment_screenshot = models.ImageField(
        upload_to='payment_screenshots/',
        storage=RawMediaCloudinaryStorage()
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - With Courier: {self.with_courier}"

