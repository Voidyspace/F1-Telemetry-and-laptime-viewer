import os
import fastf1
from fastf1 import plotting
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

#Cache setup (ignore pls)
#_________________________________________________________________________
cache_dir = os.path.join(os.path.dirname(__file__), 'f1_cache')
os.makedirs(cache_dir, exist_ok=True)

fastf1.Cache.enable_cache(cache_dir)
#_________________________________________________________________________

year = int(input("Choose a year: "))
schedule = fastf1.get_event_schedule(year).loc[:, ['RoundNumber', 'EventName', 'Country']]

print('------------------------------------------------------------------------------------------------------------------')
print(schedule)
print('------------------------------------------------------------------------------------------------------------------')

eventtype = int(input("Which event would you like to use (use RoundNo): "))
sessiontype = input("Which session (eg: FP1, Q, R): ").upper()

Session = fastf1.get_session(year, eventtype, sessiontype)
Session.load()
circuit_info = Session.get_circuit_info()

def select_lap(driver, lap):
    driver_laps = Session.laps.pick_drivers(driver)
    if lap == "":
        return driver_laps.pick_fastest()

    selected_laps = driver_laps.pick_laps(int(lap))
    if selected_laps.empty:
        print(f"No lap {lap} found for {driver}.")
        return None
    return selected_laps.iloc[0]

def comparelap():
    lap = input("Which lap would you like to view (Leave blank for fastest): ")
    driver1 = input("1st driver's lap would you like to view (Use abbreviation): ").upper()
    driver2 = input("2nd driver's lap would you like to view (Use abbreviation): ").upper()

    driver1_lap = select_lap(driver1, lap)
    if driver1_lap is None:
        return

    driver2_lap = select_lap(driver2, lap)
    if driver2_lap is None:
        return

    team1 = driver1_lap['Team']
    team2 = driver2_lap['Team']

    driver1_telemetry = driver1_lap.get_telemetry()
    driver2_telemetry = driver2_lap.get_telemetry()

    min_speed = np.min([driver1_telemetry["Speed"].min(), driver2_telemetry["Speed"].min()])
    max_speed = np.max([driver1_telemetry["Speed"].max(), driver2_telemetry["Speed"].max()])

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(driver1_telemetry["Distance"], driver1_telemetry["Speed"], label=driver1, color=fastf1.plotting.get_team_color(team1, session=Session))
    ax.plot(driver2_telemetry["Distance"], driver2_telemetry["Speed"], label=driver2, color=fastf1.plotting.get_team_color(team2, session=Session))
    ax.vlines(x = circuit_info.corners['Distance'], ymin = min_speed - 20, ymax = max_speed + 20, color = 'grey', linestyle = 'dotted')
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Speed (km/h)")

    ax.set_title(f"{Session.event['EventName']} {Session.event.year} - {Session.name}")
    ax.legend()
    plt.show()

comparelap()