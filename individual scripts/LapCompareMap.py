import os
import fastf1
from fastf1 import plotting
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

#Cache setup (ignore pls)
#_________________________________________________________________________
cache_dir = os.path.join(os.path.dirname(__file__), 'f1_cache')
os.makedirs(cache_dir, exist_ok=True)

fastf1.Cache.enable_cache(cache_dir)
#_________________________________________________________________________

Session = fastf1.get_session(2026, 18, 'Q')
Session.load()

lap = input("Which lap would you like to view (Leave blank for fastest): ")
if lap != "":
    lap = int(lap)
driver1 = input("1st driver's lap would you like to view (Use abbreviation): ").upper()
driver2 = None

def select_lap(driver):
    driver_laps = Session.laps.pick_drivers(driver)
    if lap == "":
        return driver_laps.pick_fastest()

    selected_laps = driver_laps.pick_laps(lap)
    if selected_laps.empty:
        print(f"No lap {lap} found for {driver}.")
        return None
    return selected_laps.iloc[0]

driver1_lap = select_lap(driver1)
if driver1_lap is None:
    raise SystemExit(1)

driver2_lap = select_lap(driver2) if driver2 else None
if driver2 and driver2_lap is None:
    raise SystemExit(1)

team1 = driver1_lap['Team']

team2 = driver2_lap['Team'] if driver2_lap is not None else None

driver1_telemetry = driver1_lap.get_telemetry()
if driver2_lap is None:
    driver2_telemetry = None
else:
    driver2_telemetry = driver2_lap.get_telemetry()


fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(driver1_telemetry["X"], driver1_telemetry["Y"], color='grey', alpha=0.5, label='Track' )
point1, = ax.plot([], [], 'o', color=fastf1.plotting.get_team_color(team1, session=Session), label=driver1)
if driver2_telemetry is not None:
    point2, = ax.plot([], [], 'o', color=fastf1.plotting.get_team_color(team2, session=Session), label=driver2)

def update(frame):
    x1, y1 = driver1_telemetry["X"].iloc[frame], driver1_telemetry["Y"].iloc[frame]
    point1.set_data([x1], [y1])
    if driver2_telemetry is not None:
        x2, y2 = driver2_telemetry["X"].iloc[frame], driver2_telemetry["Y"].iloc[frame]
        point2.set_data([x2], [y2])

ani = FuncAnimation(fig, update, frames = min(len(driver1_telemetry), len(driver2_telemetry)) if driver2_telemetry is not None else len(driver1_telemetry), interval=10)

ax.set_title(f"{Session.event['EventName']} {Session.event.year} - {Session.name}")
ax.legend()
plt.show()