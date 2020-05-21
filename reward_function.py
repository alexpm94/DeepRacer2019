import math

def gaussian(x, mu=0, sig=2):
    return math.exp(-math.pow(x - mu, 2.) / (2 * math.pow(sig, 2.)))

def reward_function(params):
    #Read from dictionary
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering = abs(params['steering_angle'])
    direction_stearing=params['steering_angle']
    speed = params['speed']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    is_left_of_center = params['is_left_of_center']
    
    #Define thresholds
    STEERING_THRESHOLD = 15
    SPEED_TRESHOLD = 2

    #Put a sign to the distance_center
    #if is_left_of_center:
    #    distance_from_center*=-1
    
    #reward rely on the distance_from_center
    reward_distance = gaussian(distance_from_center, mu=0, sig= track_width/2)
    
    #Waypoints
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    dx = next_point[0] - prev_point[0]
    dy = next_point[1] - prev_point[1]
    
    #atan2 can deal with dx = 0
    desired_direction = math.atan2(dy,dx)
    
    # Convert to degrees
    desired_direction =  desired_direction*(180/math.pi)
    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = desired_direction - heading
    
    #The directon reward will be multiplied by the previous reward
    reward_dir = gaussian(direction_diff, mu=0, sig = 15)
    
    if direction_diff>STEERING_THRESHOLD:
        reward_dir*=0.7
    
    if not is_left_of_center and desired_direction>heading:
        reward_dir*=0.8

    reward = reward_dir  + reward_distance
    
    #The model have difficulties when reward=0
    if not all_wheels_on_track:
        reward = 1e-3
    
    #Penalize speed
    if SPEED_TRESHOLD<2:
        reward *= 0.7
        
    if progress == 100:
        reward += 100
    
    return reward
