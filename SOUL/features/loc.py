def loc(place):
    webbrowser.open("http://www.google.com/maps/place/" + place)
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)
    if not location:
        raise ValueError(f"Location not found: {place}")
    target_latlng = location.latitude, location.longitude
    address = location.raw['address']
    target_loc = {
        'city': address.get('city', ''),
        'state': address.get('state', ''),
        'country': address.get('country', '')
    }

    current_loc = geocoder.ip('me')
    current_latlng = current_loc.latlng
    if not current_latlng:
        raise RuntimeError("Could not determine current location.")

    distance_str = str(great_circle(current_latlng, target_latlng))
    distance_km = float(distance_str.split(' ', 1)[0])
    distance = round(distance_km, 2)

    return current_loc, target_loc, distance
