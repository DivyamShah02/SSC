from django.db import models
from django.utils import timezone


class BuildingDetails(models.Model):
    building_id = models.CharField(max_length=255, unique=True)

    group_name = models.CharField(max_length=255)
    head_image = models.ImageField(upload_to='property')
    sec_image_1 = models.ImageField(upload_to='property')
    sec_image_2 = models.ImageField(upload_to='property')
    year_of_establishment = models.PositiveIntegerField()
    no_of_projects_delivered = models.PositiveIntegerField()
    key_projects = models.TextField()
    key_promoters = models.TextField()
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    alternate_name = models.CharField(max_length=255, null=True, blank=True)
    alternate_number = models.CharField(max_length=15, null=True, blank=True)
    project_id = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    developed_by = models.CharField(max_length=255)
    location_of_project = models.TextField()
    google_pin_lat = models.CharField(max_length=255, default="")  # to be filled with the current location pin
    google_pin_lng = models.CharField(max_length=255, default="")  # to be filled with the current location pin
    type_of_project = models.CharField(max_length=255)
    type_of_apartments = models.CharField(max_length=255)  # Multiple choice can be handled with a separate model if needed
    age_of_property_developer = models.PositiveIntegerField()
    age_of_property_rera = models.PositiveIntegerField()
    plot_area = models.CharField(max_length=255)
    architect = models.CharField(max_length=255)
    construction_company = models.CharField(max_length=255)
    no_of_blocks = models.PositiveIntegerField()
    no_of_units = models.PositiveIntegerField()
    no_of_floors = models.PositiveIntegerField()
    no_of_basements = models.PositiveIntegerField()
    central_air_conditioning = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)
    spiritual_or_religious_attraction = models.TextField(null=True, blank=True)
    type_of_parking = models.CharField(max_length=255)
    plc = models.DecimalField(max_digits=10, decimal_places=2)  # PLC could be a decimal field for price
    floor_rise = models.DecimalField(max_digits=10, decimal_places=2)
    development_charges = models.DecimalField(max_digits=10, decimal_places=2)  # AMC/Torrent etc
    advance_maintenance = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    other_specific_expenses = models.TextField(null=True, blank=True)
    sale_deed_value_min = models.DecimalField(max_digits=15, decimal_places=2)
    sale_deed_value_max = models.DecimalField(max_digits=15, decimal_places=2)
    gst_applicable = models.DecimalField(max_digits=4, decimal_places=2)  # GST percentage
    loan_availability = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)

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
    size_of_private_terrace = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # in square feet
    size_of_unit = models.DecimalField(max_digits=10, decimal_places=2)  # in square feet
    carpet_area_rera = models.DecimalField(max_digits=10, decimal_places=2)  # in square feet
    jodi_possible = models.BooleanField(default=False)
    no_of_attached_bathrooms = models.PositiveIntegerField()
    servant_room_available = models.BooleanField(default=False)
    separate_puja_room_available = models.BooleanField(default=False)
    no_of_balconies = models.PositiveIntegerField()
    no_of_parking_allotted = models.PositiveIntegerField()
    per_sqft_rate_saleable = models.DecimalField(max_digits=10, decimal_places=2)  # rate per square feet
    google_pin_lat = models.CharField(max_length=255, default="")  # to be filled with the current location pin
    google_pin_lng = models.CharField(max_length=255, default="")  # to be filled with the current location pin


    def __str__(self):
        return f"{self.unit_configuration} - {self.unit_type}"


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

