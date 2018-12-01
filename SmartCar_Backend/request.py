import smartcar

access_token = '5f93e4dc-50ef-4125-a78b-3867215264f2'

response = smartcar.get_vehicle_ids(access_token)

vid = response['vehicles'][0]

vehicle = smartcar.Vehicle(vid, access_token)

location = vehicle.location()

print(location)
