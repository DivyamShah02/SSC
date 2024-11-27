from django.db import models
from django.utils import timezone


class BuildingDetails(models.Model):
    building_id = models.CharField(max_length=255, unique=True)

    group_name = models.CharField(max_length=255, null=True, blank=True)
    head_image = models.ImageField(upload_to='property', null=True, blank=True)
    sec_image_1 = models.ImageField(upload_to='property', null=True, blank=True)
    sec_image_2 = models.ImageField(upload_to='property', null=True, blank=True)
    sec_image_3 = models.ImageField(upload_to='property', null=True, blank=True)
    sec_image_4 = models.ImageField(upload_to='property', null=True, blank=True)
    brochure_1 = models.FileField(upload_to='brochure', null=True, blank=True)
    brochure_2 = models.FileField(upload_to='brochure', null=True, blank=True)
    year_of_establishment = models.CharField(max_length=255, null=True, default=0, blank=True)
    no_of_projects_delivered = models.CharField(max_length=255, default=0, null=True, blank=True)

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

    number_country_code = models.CharField(max_length=10, default='', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(default='', null=True, blank=True)
    alternate_name = models.CharField(max_length=255, null=True, blank=True)
    alternate_number_country_code = models.CharField(max_length=10, default='', null=True, blank=True)
    alternate_number = models.CharField(max_length=15, null=True, blank=True)
    alternate_email = models.EmailField(default='', null=True, blank=True)
    project_id = models.CharField(max_length=255, null=True, blank=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    # developed_by = models.CharField(max_length=255, null=True, blank=True)
    location_of_project = models.TextField(null=True, blank=True)
    area_of_project = models.CharField(max_length=255, null=True, blank=True, default='')
    google_pin_lat = models.CharField(max_length=255, default="", null=True, blank=True)
    google_pin_lng = models.CharField(max_length=255, default="", null=True, blank=True)
    type_of_project = models.CharField(max_length=255, null=True, blank=True)
    per_sqft_rate_saleable = models.CharField(max_length=100, default='', null=True, blank=True)
    type_of_apartments = models.CharField(max_length=255, null=True, blank=True)

    special_amenity_1 = models.CharField(max_length=255, default='', null=True, blank=True)
    special_amenity_2 = models.CharField(max_length=255, default='', null=True, blank=True)
    special_amenity_3 = models.CharField(max_length=255, default='', null=True, blank=True)
    special_amenity_4 = models.CharField(max_length=255, default='', null=True, blank=True)

    possession_by = models.TextField(max_length=15, default='', null=True, blank=True)
    age_of_property_by_developer = models.TextField(max_length=15, default='', null=True, blank=True)
    age_of_property_rera = models.TextField(max_length=15, default='', null=True, blank=True)
    rera_approved = models.BooleanField(default=False)
    rera_by_when = models.CharField(max_length=255, null=True, blank=True)
    plot_area = models.CharField(max_length=255, null=True, blank=True)
    architect = models.CharField(max_length=255, null=True, blank=True)
    construction_company = models.CharField(max_length=255, null=True, blank=True)
    no_of_blocks = models.CharField(max_length=255, default=0, null=True, blank=True)
    no_of_units = models.CharField(max_length=255, default=0, null=True, blank=True)
    no_of_floors = models.CharField(max_length=255, default=0, null=True, blank=True)
    no_of_basements = models.CharField(max_length=255, default=0, null=True, blank=True)
    central_air_conditioning = models.CharField(max_length=255, default='', null=True, blank=True)
    # pet_friendly = models.BooleanField(default=False)
    spiritual_or_religious_attraction = models.TextField(null=True, blank=True, default='')
    type_of_parking = models.CharField(max_length=255, null=True, blank=True)
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

    unit_configuration = models.CharField(max_length=255, null=True, blank=True)
    unit_type = models.CharField(max_length=255, null=True, blank=True)
    unit_series = models.CharField(max_length=255, default='', null=True, blank=True)
    no_of_units_per_floor = models.CharField(max_length=255, default=0, null=True, blank=True)
    no_of_lifts_per_floor = models.CharField(max_length=255, default=0, null=True, blank=True)
    private_lifts = models.BooleanField(default=False)
    no_private_lifts = models.CharField(max_length=255, default=0, null=True, blank=True)
    common_terrace_accessible = models.BooleanField(default=False)
    size_of_unit = models.CharField(max_length=100, null=True, blank=True)
    carpet_area_rera = models.CharField(max_length=100, null=True, blank=True)
    jodi_possible = models.BooleanField(default=False)
    no_of_attached_bathrooms = models.CharField(max_length=255, default=0, null=True, blank=True)
    servant_room_available = models.BooleanField(default=False)
    separate_puja_room_available = models.BooleanField(default=False)
    no_of_balconies = models.CharField(max_length=255, default=0, null=True, blank=True)
    floor_to_ceiling = models.CharField(max_length=255, default=0, null=True, blank=True)

    private_terrace = models.BooleanField(default=False)
    carpet_size_terrace = models.CharField(max_length=255, default=0, null=True, blank=True)
    size_of_private_terrace_len = models.CharField(max_length=100, null=True, blank=True)
    size_of_private_terrace_wid = models.CharField(max_length=100, null=True, blank=True)

    size_of_balcony_len = models.CharField(max_length=100, null=True, blank=True, default=0)
    size_of_balcony_wid = models.CharField(max_length=100, null=True, blank=True, default=0)

    size_of_master_bedroom_len = models.CharField(max_length=100, null=True, blank=True, default=0)
    size_of_master_bedroom_wid = models.CharField(max_length=100, null=True, blank=True, default=0)

    size_of_kitchen_len = models.CharField(max_length=100, null=True, blank=True, default=0)
    size_of_kitchen_wid = models.CharField(max_length=100, null=True, blank=True, default=0)

    no_of_parking_allotted = models.CharField(max_length=255, default=0, null=True, blank=True)
    per_sqft_rate_saleable = models.CharField(max_length=100, null=True, blank=True)
    # base_price = models.CharField(max_length=100, null=True, blank=True)
    base_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    google_pin_lat = models.CharField(max_length=255, default="", null=True, blank=True)
    google_pin_lng = models.CharField(max_length=255, default="", null=True, blank=True)
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

    central_park_s_garden = models.BooleanField(default=False)
    multi_d_purpose_court = models.BooleanField(default=False)
    visitors_parking = models.BooleanField(default=False)
    gymnasium = models.BooleanField(default=False)
    splash_pool = models.BooleanField(default=False)
    outdoor_swimming_pool = models.BooleanField(default=False)
    indoor_swimming_pool = models.BooleanField(default=False)
    multi_d_purpose_hall = models.BooleanField(default=False)
    banquet_hall = models.BooleanField(default=False)
    mini_theatre = models.BooleanField(default=False)
    indoor_games = models.BooleanField(default=False)
    activity_room = models.BooleanField(default=False)
    library_s_reading_room = models.BooleanField(default=False)
    daycare_center = models.BooleanField(default=False)
    guest_rooms = models.BooleanField(default=False)
    co_d_working_space = models.BooleanField(default=False)
    skating_s_cycling_ring = models.BooleanField(default=False)
    gazebo_sit_outs = models.BooleanField(default=False)
    senior_citizen_sit_d_outs = models.BooleanField(default=False)
    walking_s_jogging_track = models.BooleanField(default=False)
    yoga_room = models.BooleanField(default=False)
    steam_sauna = models.BooleanField(default=False)
    massage_room = models.BooleanField(default=False)
    jacuzzi = models.BooleanField(default=False)
    cafeteria = models.BooleanField(default=False)
    card_room = models.BooleanField(default=False)
    toddler_play_zone = models.BooleanField(default=False)
    mud_play_zone = models.BooleanField(default=False)
    drivers_lounge = models.BooleanField(default=False)
    house_keeping_lounge = models.BooleanField(default=False)
    on_site_waste_management = models.BooleanField(default=False)
    solar_for_common_area = models.BooleanField(default=False)
    ev_charging_stations = models.BooleanField(default=False)
    green_building_rated = models.BooleanField(default=False)

    def __str__(self):
        return self.building_id

