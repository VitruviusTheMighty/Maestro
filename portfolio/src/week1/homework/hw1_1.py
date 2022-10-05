from cProfile import run
from math import sqrt

SPEED_OF_LIGHT = 299792458

def lightyears2meters(distance:float) -> float:
    """
    Converts light years to meters

        Parameters:
            distance (float): The distance in LY
        Returns:
            meters (float): The distance in Meters
    """
    meters = float(distance/0.00000000000000010570)
    return meters

def meters2lightyears(distance:float) -> float:
    """
    Converts meters to light years

        Parameters:
            distance (float): The distance in meters
        Returns:
            meters (float): The distance in LightYears
    """
    return float(distance*0.00000000000000010570)

def mps2mpy(velocity:float) -> float:
    """
    Converts meters per second to meters per year

        Parameters:
            velocity (float): The velocity in m/s
        Returns:
            velocity * num_seconds_in_one_year (float): The velocity in m/year 
    """
    seconds_in_one_year = 31557600.0
    return velocity*seconds_in_one_year

def star_travel_time(distance:float, percent_light_speed:float, approx_mass:float=70000.00)-> float:
    """
    Calculates the travel time to a star based on the distance in LY and the % speed of light an object is travelings

        Parameters:
            distance (float): The distance (in light years) to the desired star
            percent_light_speed (float): The percentage of the speed of light (299,792,458 meters/second) that we are travelling
            approx_mass (float): The approximate mass of our ship in kilograms. Default = 70K

        Returns:
            
                travel_time, new mass

            travel_time (float): The approximate travel time to the desired star in years
            new_mass (float): The approximate mass resulting from being affected by high-speed interstellar travel
    """
    if percent_light_speed<=0.0: raise Exception("You are not moving, you will never reach your destination.\nDivide by zero error, cannot calculate travel time if velocity is zero.")
    if percent_light_speed==1.0: raise Exception("Cannot move at light speed.\nDivide by zero error, cannot divide 1 / sqrt(0) to calculate factor")
    velocity = SPEED_OF_LIGHT*percent_light_speed # Our velocity is a % of the speed of light

    distance_in_meters = lightyears2meters(distance)
    inital_travel_time = distance_in_meters / mps2mpy(velocity) # We convert Meters per second to meters per year to get consistent unit in output
    
    factor = ( 1 / sqrt( ( 1 - ( (velocity**2) / (SPEED_OF_LIGHT**2) ) ) ) ) # Einstein's Equation for factor affecting mass and time based on speed

    travel_time = inital_travel_time / factor # The travel time, affected by the factor from Einstein's equations

    new_mass = approx_mass * factor # The mass, affect by the factor from Einstein's equations

    return round(travel_time,1), new_mass

def run_all_distance_simulations(percent_speed_of_light:float):
    """
    Evaluates and prints out the approximate time for traveling (in Earth years) to 

    - alpha centauri
    - barnards star
    - betelguese
    - the andromeda galaxy

        Parameters:
            percent_speed_of_light (float): 0.0 - 1.0 of the speed of light
    """
    # Distances in light years
    alpha_centauri = 4.4
    barnards_star = 6.0
    betelguese = 640
    andromeda_galaxy = 2500000
    
    # Speed constant
    percentage_of_speed_of_light = percent_speed_of_light # where 0 is 0% and 1 is 100%
    
    alpha_centauri_travel_time = star_travel_time(distance=alpha_centauri, percent_light_speed=percentage_of_speed_of_light)

    barnards_star_travel_time = star_travel_time(distance=barnards_star, percent_light_speed=percentage_of_speed_of_light)

    betelguese_travel_time = star_travel_time(distance=betelguese, percent_light_speed=percentage_of_speed_of_light)

    andromeda_galaxy_travel_time = star_travel_time(distance=andromeda_galaxy, percent_light_speed=percentage_of_speed_of_light)

    print(f"alpha_centauri: {alpha_centauri_travel_time[0]}")
    print(f"barnards star: {barnards_star_travel_time[0]}")
    print(f"betelguese: {betelguese_travel_time[0]}")
    print(f"andromeda galaxy: {andromeda_galaxy_travel_time[0]}")

if __name__ == "__main__":

    # Using 50% speed of light
    run_all_distance_simulations(percent_speed_of_light=0.5)


    # What about when using 0% speed of light?

    # run_all_distance_simulations(percent_speed_of_light=0.0)

    # It results in a divide by 0 error, obviously. 
    # If you are traveling 0mps you will never arrive anywhere

    # What about 100% speed of light?
    
    # run_all_distance_simulations(percent_speed_of_light=1.0)

    # Impossible to travel at light speed
    # Cannot calculate the factor as the factor requires you to travel at less than the speed of light



    