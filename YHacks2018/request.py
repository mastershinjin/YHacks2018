import smartcar

access_token = ''

response = smartcar.get_vehicle_ids(access_token)

vid = response['vehicles'][0]

vehicle = smartcar.Vehicle(vid, access_token)

location = vehicle.location()

print(location)
