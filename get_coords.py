from global_land_mask import globe

# Partition the norwegian coast into three buckets to avoid getting ships from swedish or british waters
out_west_to_oslo = {
    "west": 2.00,
    "east": 10.44,
    "south": 58.0,
    "north": 83.35
}
north_shift_oslo_to_sweden = {
    "west": 10.44,
    "east": 18.4,
    "south": 63.4,
    "north": 83.35
}
north_shift_sweden_to_finnmark = {
    "west": 18.4,
    "east": 29.1,
    "south": 69.0,
    "north": 83.35
}

offset = 0.1

def get_coords():
    all_coords = []
    at_sea = []
    for _map in [out_west_to_oslo, north_shift_oslo_to_sweden, north_shift_sweden_to_finnmark]:
        west = _map["west"]
        east = _map["east"]
        south = _map["south"]
        north = _map["north"]
        for lat in range(int(west * 100), int(east*100), int(100 * offset)):
            for long in range(int(south * 100), int(north * 100), int(100 * offset)):
                all_coords.append([long / 100, lat / 100, long / 100 + offset, lat / 100 + offset])
    for entry in all_coords:
        long_start, lat_start, long_end, lat_end = entry
        lat_center = (lat_start + lat_end) / 2
        long_center = (long_start + long_end) / 2
        if not globe.is_land(lat_center, long_center):
            at_sea.append(entry)
    return at_sea


def normalize_ais_coords(bbox):
    ais_coords = []

    long_start, lat_start, long_end, lat_end = bbox
    ais_coords.append([lat_start, long_start])
    ais_coords.append([lat_start, long_end])
    ais_coords.append([lat_end, long_end])
    ais_coords.append([lat_end, long_start])
    ais_coords.append([lat_start, long_start])
    return ais_coords