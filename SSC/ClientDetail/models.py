from django.db import models


class PropertyInquiry(models.Model):
    # Personal Information
    inquiry_added_by = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, default='', null=True, blank=True)
    number = models.CharField(null=True, blank=True, max_length=15)
    whatsapp_country_code = models.CharField(max_length=10, default='', null=True, blank=True)
    whatsapp = models.CharField(null=True, blank=True, max_length=15)
    email = models.EmailField(null=True, blank=True)
    profession = models.CharField(null=True, blank=True, max_length=100)
    residence = models.CharField(null=True, blank=True, max_length=200)
    reference = models.CharField(null=True, blank=True, max_length=200)
    
    # Family Demographics and Lifestyle
    why_buy_house = models.CharField(null=True, blank=True, max_length=100)
    adults = models.IntegerField(null=True, blank=True)
    children = models.IntegerField(null=True, blank=True)
    senior_citizens = models.IntegerField(null=True, blank=True)
    # have_pets = models.CharField(null=True, blank=True, max_length=10)
    current_residence_area = models.CharField(null=True, blank=True, max_length=100)
    religious_preference = models.CharField(null=True, blank=True, max_length=50)
    workplace_area = models.CharField(null=True, blank=True, max_length=100)
    school_area = models.CharField(null=True, blank=True, max_length=100)
    preferred_locations = models.CharField(null=True, blank=True, max_length=200)
    decision_driven_by = models.CharField(null=True, blank=True, max_length=20)
    dependent_on_sale = models.CharField(null=True, blank=True, max_length=10)
    looking_since = models.CharField(null=True, blank=True, max_length=50)
    time_to_seal_deal = models.CharField(null=True, blank=True, max_length=50)

    # House Specifications
    unit_type = models.CharField(max_length=255, default='', null=True, blank=True)
    bedrooms = models.CharField(null=True, blank=True, max_length=50)
    attached_washrooms = models.CharField(null=True, blank=True, max_length=50)
    servant_room = models.CharField(null=True, blank=True, max_length=10)
    puja_room = models.CharField(null=True, blank=True, max_length=10)
    min_carpet_area = models.CharField(null=True, blank=True, max_length=100)
    flats_per_floor = models.CharField(null=True, blank=True, max_length=50)
    floor_preference = models.CharField(null=True, blank=True, max_length=50)
    private_elevator = models.CharField(null=True, blank=True, max_length=10)
    central_air_conditioning = models.CharField(null=True, blank=True, max_length=10)
    min_parking_slots = models.CharField(null=True, blank=True, max_length=10)
    stack_parking = models.CharField(null=True, blank=True, max_length=50)

    # Building Preferences
    property_age = models.CharField(null=True, blank=True, max_length=50)
    society_type = models.CharField(null=True, blank=True, max_length=250)
    amenities = models.CharField(null=True, blank=True, max_length=200)

    # Finance and Timeline
    budget_min = models.CharField(null=True, blank=True, max_length=20)
    budget_max = models.CharField(null=True, blank=True, max_length=20)
    down_payment_percentage = models.CharField(null=True, blank=True, max_length=10)
    loan_approved_amount = models.CharField(null=True, blank=True, max_length=20)
    specific_needs = models.TextField(null=True, blank=True)
    concerns = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
