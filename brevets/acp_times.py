"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

# km: hrs
times_dict = { 
   200: 13.5,
   300: 20,
   400: 27,
   600: 40,
   1000: 75 
}

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
    max_distance = False
    
    if control_dist_km == 0: 
       return brevet_start_time
    
    if control_dist_km > brevet_dist_km:
       max_distance = True
       
    time = 0
    interval = 0
    max_interval = 3
    max_speed = [34, 32, 30, 28]
    distance_intervals = [200, 200, 200, 400]
    while (control_dist_km > 0):
       if (control_dist_km > distance_intervals[interval]):
          value_to_divide = distance_intervals[interval]
       else:
          if max_distance: # If control_dist_km > brevet_dist_km then we don't want to add additional time - all calculations have been done now
             break
          else:
            value_to_divide = control_dist_km
      
       time += (value_to_divide/max_speed[interval])
       control_dist_km -= distance_intervals[interval] 
       
       if (interval != max_interval):
         interval += 1
    
    seconds = convert_time(time) 
    
    return brevet_start_time.shift(seconds=+seconds)
        


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
        
    if control_dist_km == 0: 
       return brevet_start_time.shift(hours=+1)
    
    if control_dist_km >= brevet_dist_km:
       shift_time = times_dict[brevet_dist_km]
       return brevet_start_time.shift(hours=+shift_time)
    
    time = 0
    interval = 0
    max_interval = 1
    max_speed = [15, 11.428]
    distance_intervals = [600, 400]
    while (control_dist_km > 0):    
       if (control_dist_km > distance_intervals[interval]):
          value_to_divide = distance_intervals[interval]
       else:
          value_to_divide = control_dist_km
          
       time += (value_to_divide/max_speed[interval])
       control_dist_km -= distance_intervals[interval] 
       
       if (interval != max_interval): 
         interval += 1
         
       
    seconds = convert_time(time)
    
    return brevet_start_time.shift(seconds=+seconds)
 

def convert_time(time):
    seconds = 3600 * time
    if (seconds % 60 >= 30): # Check if rounding is needed
       seconds_to_add = 60 - (seconds % 60)
       seconds += seconds_to_add
     
    return seconds  