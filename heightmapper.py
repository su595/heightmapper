import numpy as np
from PIL import Image
from math import sin, cos, sqrt, atan2
import requests
import json

DREISAM_UL = (48.154658, 7.615669)
DREISAM_LR = (47.861023, 8.055387)
UL_FUJI = (35.49495, 138.56429) # sample coordinates
LR_FUJI = (35.24691, 138.88908)
PATH = "/home/yannick/Pictures/" # picture output path, including a / at the end
MAX_API_CALLS = 1000000 # to avoid waiting for 10mins for one picture
POINTS_PER_ITERATION = 800 # 800 is a good value


# upper_left_corner and lower_right_corner are coordinate points (latitude, longitude) forming the boundaries of a rectangular heightmap 
# scale is meters per pixel (limited to ~100 by underlying data)
# path is the destination of the generated heightmap
def make_heightmap(ul_corner,lr_corner, scale, path=False):

    distance_x = get_distance_between_coords(ul_corner, (ul_corner[0], lr_corner[1]))
    distance_y = get_distance_between_coords(ul_corner, (lr_corner[0], ul_corner[1]))
    print(distance_x)
    print(distance_y)
    pixels_x = distance_x//scale # integer division, fractions will be truncated
    pixels_y = distance_y//scale

    lat_steps = (ul_corner[0] - lr_corner[0]) / pixels_y # change in lat and lon per pixel
    lon_steps = abs((ul_corner[1] - lr_corner[1]) / pixels_x) # abs doesn't mess anything up if ul and lr are correct
    
    print(lat_steps)
    print(lon_steps)

    # safety stop
    if (pixels_y*pixels_x) > MAX_API_CALLS:
        # this doesn't prevent naturally large maps with reasonable scale, but only maps with unreasonable scale
        print("Scale is too small, the image would have {0} individual pixels! (more than {1}! :O) ".format(pixels_x*pixels_y, MAX_API_CALLS))
        return

    confirm = input("This will produce an image of {0}*{1} pixels with a total of {2} pixels, are you sure? (y/N) ".format(pixels_x, pixels_y, pixels_x*pixels_y))
    # if the input is not exactly y or Y, end the funtion here
    if confirm.upper() != "Y":
        return

    # goes through the rectangle by lat_steps and lon_steps -steps and appends the points from up to down and left to right 
    point_list = []
    for i_y in range(pixels_y):
        for i_x in range(pixels_x):
            point_list.append((ul_corner[0] - (lat_steps*i_y), ul_corner[1] + (lon_steps*i_x)))

    # get the elevation at each point
    elevation = post_elevations(point_list)
    min_elevation = min(elevation)
    max_elevation = max(elevation)
    
    map_array = np.full((pixels_y,pixels_x), 0, dtype=np.uint8)
    main_i = 0
    for i_y in range(pixels_y):
        for i_x in range(pixels_x):
            # map the elevations relative to min_ and max_elevation to a uint_8
            # in the correct order for Image.fromarray
            map_array[i_y, i_x] = map_range(elevation[main_i], min_elevation, max_elevation, 0, 255)

            main_i += 1

    # L specifies a black-white picture
    heightmap = Image.fromarray(map_array, 'L')
    heightmap.show()

    # if path was given and isn't the default False
    if path:
        heightmap.save("{0}{1},{2},{3}.png".format(path, ul_corner[0], ul_corner[1], scale), format="PNG")

def post_elevations(point_list): # returns a list of elevations for the points using api.open-elevation.com
    iterations = ((len(point_list) - len(point_list)%POINTS_PER_ITERATION)//POINTS_PER_ITERATION) + 1
    all_temp_elevations = []
    point_i = 0
    for iteration_no in range(iterations):
        # progress meter
        print(".", end="")
        temp_elevations = []
        data = {"locations": []}

        # divides the point_list into smaller lists that can be sent to the api via a post request
        # problems occur when sending more than around 800 points at onnce
        while point_i < (iteration_no+1) * POINTS_PER_ITERATION:
            # when the end of the point list is reached, stop the loop
            if point_i >= len(point_list):
                break
            data["locations"].append({"latitude": point_list[point_i][0], "longitude": point_list[point_i][1]})
            point_i += 1

        json_data = json.dumps(data, indent=4)

        newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.post("https://api.open-elevation.com/api/v1/lookup", data=json_data, headers=newHeaders)

        for result in response.json()["results"]:
            temp_elevations.append((result["elevation"]))
        
        all_temp_elevations.append(temp_elevations)
    
    # combines the smaller temp_elevations into one large elevations list
    elevations = []
    for temp_elevations in all_temp_elevations:
        for elevation in temp_elevations:
            elevations.append(elevation)
            
    return elevations

def map_range(val, in_min, in_max, out_min, out_max): # map val proportionally to new range, just like arduino map() function
    return (val - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
def get_distance_between_coords(coord1, coord2): # returns the absolute distance between 2 coordinates, accurate to 4 sf
    # everything to 4 sf
    # source: https://www.movable-type.co.uk/scripts/latlong.html
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    R = 6371000 # radius of the earth in metres
    PI = 3.142

    φ1 = lat1 * PI/180 # convert to radians  φ, λ in radians
    φ2 = lat2 * PI/180
    Δφ = (lat2-lat1) * PI/180
    Δλ = (lon2-lon1) * PI/180

    a = sin(Δφ/2) * sin(Δφ/2) + cos(φ1) * cos(φ2) * sin(Δλ/2) * sin(Δλ/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a)) # angular distance 

    return int(round(R * c, 0)) # in whole metres


make_heightmap(UL_FUJI,LR_FUJI, 200, PATH)

