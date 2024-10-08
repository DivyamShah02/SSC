from django.db import models
from django.utils import timezone


class BuildingDetails(models.Model):
    building_id = models.CharField(max_length=255, unique=True)

    group_name = models.CharField(max_length=255)
    head_image = models.ImageField(upload_to='property', null=True, blank=True)
    sec_image_1 = models.ImageField(upload_to='property', null=True, blank=True)
    sec_image_2 = models.ImageField(upload_to='property', null=True, blank=True)
    sec_image_3 = models.ImageField(upload_to='property', null=True, blank=True)
    sec_image_4 = models.ImageField(upload_to='property', null=True, blank=True)
    brochure_1 = models.FileField(upload_to='brochure', null=True, blank=True)
    brochure_2 = models.FileField(upload_to='brochure', null=True, blank=True)
    year_of_establishment = models.PositiveIntegerField()
    no_of_projects_delivered = models.PositiveIntegerField()

    key_projects_1 = models.CharField(max_length=255, default='', null=True, blank=True)
    key_projects_2 = models.CharField(max_length=255, default='', null=True, blank=True)
    key_projects_3 = models.CharField(max_length=255, default='', null=True, blank=True)
    key_projects_4 = models.CharField(max_length=255, default='', null=True, blank=True)
    key_projects_5 = models.CharField(max_length=255, default='', null=True, blank=True)
    
    key_promoters_1 = models.CharField(max_length=255, default='', null=True, blank=True)
    key_promoters_2 = models.CharField(max_length=255, default='', null=True, blank=True)
    key_promoters_3 = models.CharField(max_length=255, default='', null=True, blank=True)
    key_promoters_4 = models.CharField(max_length=255, default='', null=True, blank=True)
    key_promoters_5 = models.CharField(max_length=255, default='', null=True, blank=True)

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    email = models.EmailField(default='', null=True, blank=True)
    alternate_name = models.CharField(max_length=255, null=True, blank=True)
    alternate_number = models.CharField(max_length=15, null=True, blank=True)
    alternate_email = models.EmailField(default='', null=True, blank=True)
    project_id = models.CharField(max_length=255, null=True, blank=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    developed_by = models.CharField(max_length=255, null=True, blank=True)
    location_of_project = models.TextField(null=True, blank=True)
    google_pin_lat = models.CharField(max_length=255, default="") 
    google_pin_lng = models.CharField(max_length=255, default="") 
    type_of_project = models.CharField(max_length=255)
    per_sqft_rate_saleable = models.CharField(max_length=100, default='')
    type_of_apartments = models.CharField(max_length=255)

    special_amenity_1 = models.CharField(max_length=255, default='', null=True, blank=True)
    special_amenity_2 = models.CharField(max_length=255, default='', null=True, blank=True)
    special_amenity_3 = models.CharField(max_length=255, default='', null=True, blank=True)
    special_amenity_4 = models.CharField(max_length=255, default='', null=True, blank=True)

    possession_by = models.TextField(max_length=15, default='', null=True, blank=True)
    age_of_property_by_developer = models.TextField(max_length=15, default='', null=True, blank=True)
    age_of_property_rera = models.TextField(max_length=15, default='', null=True, blank=True)
    rera_approved = models.BooleanField(default=False)
    plot_area = models.CharField(max_length=255)
    architect = models.CharField(max_length=255)
    construction_company = models.CharField(max_length=255)
    no_of_blocks = models.PositiveIntegerField()
    no_of_units = models.PositiveIntegerField()
    no_of_floors = models.PositiveIntegerField()
    no_of_basements = models.PositiveIntegerField()
    central_air_conditioning = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)
    spiritual_or_religious_attraction = models.TextField(null=True, blank=True, default='')
    type_of_parking = models.CharField(max_length=255)
    plc_garden = models.CharField(max_length=20, default=0, blank=True, null=True)
    plc_road_facing = models.CharField(max_length=20, default=0, blank=True, null=True)
    plc_corner = models.CharField(max_length=20, default=0, blank=True, null=True)
    plc_others = models.CharField(max_length=20, default=0, blank=True, null=True)
    floor_rise = models.TextField(null=True, blank=True)
    development_charges = models.CharField(max_length=20, default=0, blank=True, null=True)
    advance_maintenance = models.CharField(max_length=20, default=0, blank=True, null=True)
    maintenance_deposit = models.CharField(max_length=20, default=0, blank=True, null=True)
    other_specific_expenses = models.CharField(max_length=20, default=0, null=True, blank=True)
    sale_deed_value = models.CharField(max_length=20, default=0, blank=True, null=True)
    sale_deed_value_min = models.CharField(max_length=20, default=0, blank=True, null=True)
    sale_deed_value_max = models.CharField(max_length=20, default=0, blank=True, null=True)
    gst_applicable = models.CharField(max_length=20, default=0, blank=True, null=True)
    loan_availability = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group_name} - {self.project_name}"


class UnitDetails(models.Model):
    building_id = models.CharField(max_length=255)

    unit_configuration = models.CharField(max_length=255)
    unit_type = models.CharField(max_length=255)
    no_of_units_per_floor = models.PositiveIntegerField()
    no_of_lifts_per_floor = models.PositiveIntegerField()
    private_lifts = models.BooleanField(default=False)
    common_terrace_accessible = models.BooleanField(default=False)
    size_of_private_terrace = models.CharField(max_length=100, null=True, blank=True)
    size_of_unit = models.CharField(max_length=100)
    carpet_area_rera = models.CharField(max_length=100)
    jodi_possible = models.BooleanField(default=False)
    no_of_attached_bathrooms = models.PositiveIntegerField()
    servant_room_available = models.BooleanField(default=False)
    separate_puja_room_available = models.BooleanField(default=False)
    no_of_balconies = models.PositiveIntegerField()
    size_of_balcony = models.CharField(max_length=100, null=True, blank=True, default=0)
    size_of_master_bedroom = models.CharField(max_length=100, null=True, blank=True, default=0)
    size_of_kitchen = models.CharField(max_length=100, null=True, blank=True, default=0)
    no_of_parking_allotted = models.PositiveIntegerField()
    per_sqft_rate_saleable = models.CharField(max_length=100)
    base_price = models.CharField(max_length=100, null=True, blank=True)
    google_pin_lat = models.CharField(max_length=255, default="")
    google_pin_lng = models.CharField(max_length=255, default="")
    floor_plan = models.ImageField(upload_to='plan', null=True, blank=True)
    unit_plan = models.ImageField(upload_to='plan', null=True, blank=True)
    active = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.unit_configuration} - {self.unit_type}"
    
    # def save(self, *args, **kwargs):
    #     self.base_price = self.size_of_unit * self.per_sqft_rate_saleable
    #     super(UnitDetails, self).save(*args, **kwargs)


class Amenities(models.Model):
    building_id = models.CharField(max_length=255, unique=True)

    swimming_pool = models.BooleanField(default=False)
    gym_fitness_center = models.BooleanField(default=False)
    clubhouse = models.BooleanField(default=False)
    children_play_area = models.BooleanField(default=False)
    sports_facilities = models.BooleanField(default=False)
    jogging_walking_tracks = models.BooleanField(default=False)
    common_gardens = models.BooleanField(default=False)
    community_hall = models.BooleanField(default=False)
    security_24_7 = models.BooleanField(default=False)
    cctv_surveillance = models.BooleanField(default=False)
    power_backup = models.BooleanField(default=False)
    waste_management = models.BooleanField(default=False)
    concierge = models.BooleanField(default=False)
    reading_room = models.BooleanField(default=False)
    home_theatre = models.BooleanField(default=False)
    internet_connectivity = models.BooleanField(default=False)
    guest_rooms = models.BooleanField(default=False)
    pet_friendly_areas = models.BooleanField(default=False)
    spa_salon = models.BooleanField(default=False)
    co_working_space = models.BooleanField(default=False)
    terrace_amenities = models.BooleanField(default=False)

    def __str__(self):
        return self.building_id

