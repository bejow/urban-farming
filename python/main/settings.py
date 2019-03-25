#default settings for the Plants
system_settings = {
    "light_time": 7200,
    "no_light_time" : 7200,
    "water_time" : 5,
    "no_water_time": 2, 
}

#programm settings

update_ph_frequency = 60
update_oxygen_frequency = 60
update_temperature_frequency = 60
fetch_settings_frequency = 3
water_relais_pin = 13
light_relais_pin = 11


#api settings
api_url = "http://192.168.1.21:3000/"
settings_endpoint = "settings"
ph_endpoint = "ph"
oxygen_endpoint = "oxygen"
temperature_endpoint = "temperature"
