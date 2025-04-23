from django.db import models

class CandidateBiodata(models.Model):
    # Personal Details
    candidate_name = models.CharField(max_length=255)
    dob = models.DateField()
    marital_status = models.CharField(max_length=50)
    disability = models.CharField(max_length=255, blank=True, null=True)
    birth_time = models.TimeField(blank=True, null=True)
    birth_place = models.CharField(max_length=255)
    current_city_country = models.CharField(max_length=255)
    visa_status = models.CharField(max_length=255, blank=True, null=True)
    children = models.CharField(max_length=255, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)
    education = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    monthly_income = models.CharField(max_length=100, blank=True, null=True)
    shani_mangal = models.CharField(max_length=50, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)

    # Contact Details
    email = models.EmailField(max_length=254)
    whatsapp_number = models.CharField(max_length=20)


    # Habits & Declaration
    eating_habits = models.CharField(max_length=50, blank=True, null=True)
    alcoholic_drinks = models.BooleanField(default=False)
    smoke = models.BooleanField(default=False)
    other_habits = models.TextField(blank=True, null=True)
    legal_police_case = models.BooleanField(default=False)

    # Family Details
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    father_mobile = models.CharField(max_length=20)
    mother_mobile = models.CharField(max_length=20)
    parents_residence_city = models.CharField(max_length=255)
    type_of_brahmin = models.CharField(max_length=255, blank=True, null=True)
    gotra = models.CharField(max_length=255, blank=True, null=True)
    kuldevi = models.CharField(max_length=255, blank=True, null=True)
    siblings = models.CharField(max_length=255, blank=True, null=True)

    # Partner Preferences
    partner_location = models.CharField(max_length=255, blank=True, null=True)
    partner_age_bracket = models.CharField(max_length=100, blank=True, null=True)
    partner_education = models.CharField(max_length=255, blank=True, null=True)
    other_specific_choice = models.TextField(blank=True, null=True)

    # Photograph
    photograph = models.ImageField(upload_to='photographs/')

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_name
