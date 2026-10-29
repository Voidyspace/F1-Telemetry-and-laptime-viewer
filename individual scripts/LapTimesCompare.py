import os
import fastf1
from fastf1 import plotting
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt

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

session = fastf1.get_session(year, eventtype, sessiontype)
session.load()

driver1 = input("1st driver's lap times would you like to view (Use abbreviation): ").upper()
driver2 = input("2nd driver's lap times would you like to view (Use abbreviation)(Optional): ").upper()

fig, ax = plt.subplots(figsize=(8, 5))

for driver in [driver1, driver2]:
    laps = session.laps.pick_drivers(driver).pick_quicklaps().reset_index()
    style = plotting.get_driver_style(identifier=driver,
                                      style=["color", "linestyle"],
                                      session=session)
    ax.plot(laps["LapTime"], **style, label=driver)

ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")
ax.set_title(f"{session.event['EventName']} {session.event.year} - {session.name}")
ax.legend()
plt.show()