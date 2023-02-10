"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
from datetime import timedelta

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    
    # Cases:
    # 
    # Case 1:
    #   If control_dist_km is 0 then the open time is simply the brevet_start_time
    #
    # Case 2:
    #   If control_dist_km > brevet_dist_km by 20% 
    #     Return error - "Too far over theoretical distance"
    # 
    # Case 3+: 
    #   Check control_dist_km and break it up respectively
    #   Ex: if dist = 500 --> break it up into 200, 200, 100 and divide
    #   by respective max speeds
    #   Ex: if dist = 1100 --> 200, 200, 200, 400, 100
    
    max_control_dist = brevet_dist_km * 1.2 # This is used to make sure our control distance isn't more than 20% of our estimated race distance
    
    if control_dist_km == 0: 
       return brevet_start_time
    
    if control_dist_km > max_control_dist: 
       return arrow.now()
      
   
    time = 0
    interval = 0
    max_speed = [34, 32, 30, 28, 26]
    distance_intervals = [200, 200, 200, 400, 300]
    while (control_dist_km > 0):
       if (control_dist_km > distance_intervals[interval]):
          value_to_divide = distance_intervals[interval]
       else:
          value_to_divide = control_dist_km
      
       time += (value_to_divide/max_speed[interval])
       control_dist_km -= distance_intervals[interval] 
       interval += 1
    
    converted_time = convert_time(time) 
    
    updated_time = brevet_start_time + converted_time  
        
    return updated_time


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    # Cases:
    # 
    # Case 1:
    #   If control_dist_km is 0 then the close time is simply an hour after
    #
    # Case 2:
    #   If control_dist_km > brevet_dist_km by 20% 
    #     Return error - "Too far over theoretical distance"
    # 
    # Case 3+: 
    #   Check control_dist_km and break it up respectively
    #   Ex: if dist = 500 --> break it up into 200, 200, 100 and divide
    #   by respective max speeds
    #   Ex: if dist = 1100 --> 200, 200, 200, 400, 100
        
    if control_dist_km == 0: 
       return brevet_start_time + timedelta(hours=1)
    
    time = 0
    interval = 0
    max_speed = [15, 11.428, 13.333]
    distance_intervals = [600, 400, 300]
    while (control_dist_km > 0):    
       if (control_dist_km > distance_intervals[interval]):
          value_to_divide = distance_intervals[interval]
       else:
          value_to_divide = control_dist_km
          
       time += (value_to_divide/max_speed[interval])
       control_dist_km -= distance_intervals[interval] 
       interval += 1
       
    converted_time = convert_time(time)
    
    updated_time = brevet_start_time + converted_time
    
    return updated_time
 

def convert_time(time):
    seconds = 3600 * time
    if (seconds % 60 >= 30): # Check if rounding is needed
       seconds_to_add = 60 - (seconds % 60)
       seconds += seconds_to_add
       
    return timedelta(seconds=seconds)