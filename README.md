# DeepRacer2019
This repo contains the necessary informacion to compete in Deep Racer League by Amazon.

# What is Deep Racer League?
It is an online competition about self-driving cars hosted by Amazon.

# How do I compete?
You just need an Amazon account and look forward to learn about Reinforcement Learning.
Amazon gives 10 hours for free, to train your own models each month.

# Do I need any specific background?
You just need to know a little bit about python programing. You don't need any background on AI!
As all the algorithms and data sensor acquisition is already provided by amazon
All you need is to create a "Reward Function".

# How does it work?
You need to create a Reinforcement Learning model.
This algorithm is based in giving positive or negative rewards to the system, depending on its performance.
For example, if the car stays in lane, you must give a positive reward. If it gets out of lane, you must give a negative reward.
For a deeper explanation visit [this link](https://d2k9g1efyej86q.cloudfront.net/).

# How do I train the model?
Is pretty easy and straight forward. Amazon gives an amazing tutorial in this [get started tutorial](https://console.aws.amazon.com/deepracer/home?region=us-east-1#getStarted).

# Action Space
You must indicate the possible states it can take. It is a combitation of speed and staring angle.
Remember, this is not a classic control problem.
![Action space](/images/action.JPG)

# Data sensors
Data | Explanation
------------ | -------------
x and y	| The position of the vehicle on the track
heading |	Orientation of the vehicle on the track
waypoints |	List of waypoint coordinates
closest_waypoints	| Index of the two closest waypoints to the vehicle
progress | Percentage of track completed
steps	| Number of steps completed
track_width	| Width of the track
distance_from_center |	Distance from track center line
is_left_of_center	| Whether the vehicle is to the left of the center line
all_wheels_on_track |	Is the vehicle completely within the track boundary?
speed	| Observed speed of the vehicle
steering_angle | Steering angle of the front wheels

# Waypoints
Waypoints are marks along the road thar allows the car to know where it is located in the road.
![waypoints img](/images/waypoints.JPG)

# My reward Function.
There are many aproaches. Amazon already provide three in which you can work on.
One is just to reward positively just if the car stays in lane.
My aproach is to reward the car according to its current heading and its distance to the center.
One of the data given is the heading. This show us the current heading of the car.
As we also have the way points, we can calculate the "desired heading" the car is supposed pointing.

```python
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
```
Now we have the direction error or direction difference, we must reward the system.
I inspired my logic in a fuzzy control. I used a gaussian function to map the reward values.

![Gaussian image](/images/gaussian.JPG)

The error can go from -Pi to Pi. The closest to zero, the higher the reward.

In order to avoid abrupt changes, I rewarded in an even lower rate if the difference is bigger than 15 dgrees.
```python
   if direction_diff>STEERING_THRESHOLD:
        reward_dir*=0.7
```

# Tips to get good Results

 * It is recomended to train a model for at least 3 hours. Five hours use to present a better result in my case.
 * Do not use a big action space, as it takes longer to traing and overfit the model.
 * Try to use most of given data. It is provided for something...
