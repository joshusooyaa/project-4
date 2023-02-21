# RUSA ACP Control Time Calculator
## `acp_times.py`
`acp_times.py` Contains two main functions, `open_time` and `close_time`. These two functions calculate the open and close time of the distances provided. 

`open_time` has several rules.
1. If the distance is 0km it returns the start time of the race
2. If the distance is greater than the brevet distance, then it'll make sure to only return a time calculated up to the brevet distance (so if the distance is 305 km, it'll only calculate for 300km)
3. Otherwise, the time is calculated using distance intervals with their associated speeds. 

`close_time` follows a similar structure.
1. If the distance is 0km it returns 1 hour after the start time
2. If the distance is greater than the brevet distance then it'll make sure to return a fixed value for that brevet_distance. 
3. If the distance is <= 60 then the time is calculated by distance/20 + 1 and that is used to shift the time. 

All time is in YYYY-MM-DDTHH:MM format and must stay in this format. Both functions ensure that this format is kept by using arrow time and using the shift function the adjust the time. `brevet_start_time` is what gets shifted - as we are calculating the time based off of the beginning of the race each time. 

## `flask_brevets.py`
`flask_brevets.py` is updated to make sure the correct control distance and time is passed in so `acp_times.py` can calculate the correct times. For `flask_brevets.py` to pass a control distance, start time and brevet distance, it needs to get the information from the webpage (specifically from the JSON HTTP request) - so it uses request.args.get(). These arguments are passed in the Javascript from the getJSON request in `calc.html`. Using these arguments, they are then saved as variables in `flask_brevets.py` and are passed to the functions in `acp_times.py` to get the correct time calculations. Once this is done, the open and close times are saved and passed back to the Javascript in `calc.html` as a JSON file. 

## `calc.html`
`calc.html` has been updated to make sure that the necesarry information is passed to `flask_brevets.py`. It does this by collecting the brevet distance (km) from the page, as well as the begin_date. The KM was already implemented, but that is also collected. These are then passed as arguments when sending the JSON HTTP request.
 
Once the `flask_brevets.py` sends a response back (sending the JSON back) it unpacks the information (open and close time) and updates the HTML with the open and close time that. 

-----
Josh Sawyer\
jsawyer2@uoregon.edu

