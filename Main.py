import os
import fastf1
from fastf1 import plotting
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

#defenitions
def select_lap(driver, lap):
    driver_laps = Session.laps.pick_drivers(driver)
    if lap == "":
        return driver_laps.pick_fastest()

    selected_laps = driver_laps.pick_laps(int(lap))
    if selected_laps.empty:
        print(f"No lap {lap} found for {driver}.")
        return None
    return selected_laps.iloc[0]

def viewlaptimes():
    driver = input("Which driver's laps would you like to view (Use abbreviation): ").upper()

    print('--------------------------------------------------------------------------------------------------------')
    print("Fastest lap:", Session.laps.pick_drivers(driver).pick_fastest())
    print('--------------------------------------------------------------------------------------------------------')
    print(Session.laps.pick_drivers(driver).loc[:, ['LapTime', 'Compound', 'TyreLife', 'Deleted', 'Sector1Time', 'Sector2Time', 'Sector3Time']])
    print('--------------------------------------------------------------------------------------------------------')

def viewlaptelegraph():
    lap = input("Which lap would you like to view (Leave blank for fastest): ")
    driver1 = input("Which driver's lap would you like to view (Use abbreviation): ").upper()

    driver1_lap = select_lap(driver1, lap)
    if driver1_lap is None:
        return

    team1 = driver1_lap['Team']
    
    driver1_telemetry = driver1_lap.get_telemetry()

    min_speed = driver1_telemetry["Speed"].min()
    max_speed = driver1_telemetry["Speed"].max()
    throttlepercent = (driver1_telemetry["Throttle"]/100)*350
    brakepercent = (driver1_telemetry["Brake"])*350
 
    fig, ax = plt.subplots(figsize=(8, 5))
    ax2 = ax.twinx()


    ax2.plot(driver1_telemetry["Distance"], throttlepercent, color='Green', alpha=0.5, linestyle='dashed')

    
    ax.plot(driver1_telemetry["Distance"], driver1_telemetry["Speed"], color='Blue', label= " Speed")
    
    ax2.plot(driver1_telemetry["Distance"], brakepercent, color= 'Red',alpha=0.5, linestyle='dashed', label= " Throttle/Brakes")
    
    ax.vlines(x = circuit_info.corners['Distance'], ymin = min_speed - 20, ymax = max_speed + 20, color = 'grey', linestyle = 'dotted')
    
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Speed (km/h)")
    ax2.set_ylabel("Brake/Throttle (%)")

    ax.set_title(f"{Session.event['EventName']} {Session.event.year} - {Session.name}({driver1})")
    ax.legend(loc='upper left',
          ncol=3, fancybox=True, shadow=True)
    if input("Would you like to save this graph? (y/n): ").lower() == "y":
        plt.savefig(f"{Session.event['EventName']}_{Session.event.year}_{Session.name}_{driver1}_lap_telemetry.png")
    plt.show()

def comparelapspeedgraph():
    lap = input("Which lap would you like to view (Leave blank for fastest): ")
    driver1 = input("1st driver's lap would you like to view (Use abbreviation): ").upper()
    driver2 = input("2nd driver's lap would you like to view (Use abbreviation)(Optional): ").upper()

    driver1_lap = select_lap(driver1, lap)
    if driver1_lap is None:
        return

    driver2_lap = select_lap(driver2, lap) if driver2 else None
    if driver2 and driver2_lap is None:
        return

    team1 = driver1_lap['Team']
    
    team2 = driver2_lap['Team'] if driver2_lap is not None else None

    driver1_telemetry = driver1_lap.get_telemetry()
    if driver2_lap is None:
        driver2_telemetry = None   
    else:
        driver2_telemetry = driver2_lap.get_telemetry()

    if driver2_telemetry is None:
        min_speed = driver1_telemetry["Speed"].min()
        max_speed = driver1_telemetry["Speed"].max()
    else:
        min_speed = np.min([driver1_telemetry["Speed"].min(), driver2_telemetry["Speed"].min()])
        max_speed = np.max([driver1_telemetry["Speed"].max(), driver2_telemetry["Speed"].max()])

    fig, ax = plt.subplots(figsize=(8, 5))

    if driver2_telemetry is None:
        ax.plot(driver1_telemetry["Distance"], driver1_telemetry["Speed"], label=driver1, color=fastf1.plotting.get_team_color(team1, session=Session))
    else:
        ax.plot(driver1_telemetry["Distance"], driver1_telemetry["Speed"], label=driver1, color=fastf1.plotting.get_team_color(team1, session=Session))
        ax.plot(driver2_telemetry["Distance"], driver2_telemetry["Speed"], label=driver2, color=fastf1.plotting.get_team_color(team2, session=Session))


    ax.vlines(x = circuit_info.corners['Distance'], ymin = min_speed - 20, ymax = max_speed + 20, color = 'grey', linestyle = 'dotted')
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Speed (km/h)")


    ax.set_title(f"{Session.event['EventName']} {Session.event.year} - {Session.name}")
    ax.legend(loc='upper left',
          ncol=3, fancybox=True, shadow=True)
    if input("Would you like to save this graph? (y/n): ").lower() == "y":
        plt.savefig(f"{Session.event['EventName']}_{Session.event.year}_{Session.name}_lap_comparison.png")
    plt.show()

def comparelaptimesgraph():
    driver1 = input("1st driver's lap times would you like to view (Use abbreviation): ").upper()
    driver2 = input("2nd driver's lap times would you like to view (Use abbreviation): ").upper()

    fig, ax = plt.subplots(figsize=(8, 5))

    for driver in [driver1, driver2]:
        laps = Session.laps.pick_drivers(driver).pick_quicklaps().reset_index()
        style = plotting.get_driver_style(identifier=driver,
                                        style=["color", "linestyle"],
                                        session=Session)
        ax.plot(laps["LapTime"], **style, label=driver)

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    ax.set_title(f"{Session.event['EventName']} {Session.event.year} - {Session.name}")
    ax.legend(loc='upper left',
        ncol=3, fancybox=True, shadow=True)
    if input("Would you like to save this graph? (y/n): ").lower() == "y":
        plt.savefig(f"{Session.event['EventName']}_{Session.event.year}_{Session.name}_lap_comparison.png")
    plt.show()

def comparelaptimemap():
    lap = input("Which lap would you like to view (Leave blank for fastest): ")
    driver1 = input("1st driver's lap would you like to view (Use abbreviation): ").upper()
    driver2 = input("2nd driver's lap would you like to view (Use abbreviation)(Optional): ").upper()

    driver1_lap = select_lap(driver1, lap)
    if driver1_lap is None:
        return

    driver2_lap = select_lap(driver2, lap) if driver2 else None
    if driver2 and driver2_lap is None:
        return

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

    ani = FuncAnimation(fig, update, frames = min(len(driver1_telemetry), len(driver2_telemetry)) if driver2_telemetry is not None else len(driver1_telemetry), interval=100)

    ax.set_title(f"{Session.event['EventName']} {Session.event.year} - {Session.name}")
    ax.legend(loc='upper left',
          ncol=3, fancybox=True, shadow=True)
    if input("Would you like to save this animation? (y/n): ").lower() == "y":
        ani.save(filename=f"{Session.event['EventName']}_{Session.event.year}_{Session.name}_lap_map_comparison.mp4", writer='ffmpeg', fps=10)
    plt.show()

def viewtelebar():
    lap = input("Which lap would you like to view (Leave blank for fastest): ")
    driver1 = input("which driver's lap would you like to view (Use abbreviation): ").upper()

    driver1_lap = select_lap(driver1, lap)
    if driver1_lap is None:
        return

    team1 = driver1_lap['Team']
    driver1_telemetry = driver1_lap.get_telemetry()

    fig, ax = plt.subplots(figsize=(8, 5))

    categories = ['Speed', 'Throttle', 'Brake']
    y_data = [driver1_telemetry["Speed"].iloc[0], driver1_telemetry["Throttle"].iloc[0]*3.5, driver1_telemetry["Brake"].iloc[0]*350]
    bars = ax.bar(categories, y_data, color=['tab:blue', 'tab:red', 'tab:green'])


    def update(frame):
        new_data = [driver1_telemetry["Speed"].iloc[frame], driver1_telemetry["Throttle"].iloc[frame]*3.5, driver1_telemetry["Brake"].iloc[frame]*350]
        for bar, height in zip(bars, new_data):
            bar.set_height(height)
        

    ani = FuncAnimation(fig, update, frames = min(len(driver1_telemetry), len(driver1_telemetry)), interval=100)

    ax.set_title(f"{Session.event['EventName']} {Session.event.year} - {Session.name}, {driver1} throttle/brake/speed comparison")
    ax.legend(loc='upper left',
          ncol=3, fancybox=True, shadow=True)
    if input("Would you like to save this animation? (y/n): ").lower() == "y":
        ani.save(filename=f"{Session.event['EventName']}_{Session.event.year}_{Session.name}_lap_telemetry.mp4", writer='ffmpeg', fps=10)
    plt.show()

#Cache setup
#_________________________________________________________________________
cache_dir = os.path.join(os.path.dirname(__file__), 'f1_cache')
os.makedirs(cache_dir, exist_ok=True)

fastf1.Cache.enable_cache(cache_dir)
#_________________________________________________________________________

#actual program
print('--------------------------------------------------------------------------------------------------------')
print("F1 telemetry and laptime viewing tool (By @Voidyspace on github)")
print("This tool uses the fastf1 library to access F1 telemetry data and laptimes")
print("Note: all generated graphs and maps (if saved) will be saved in the current working directory")
print('--------------------------------------------------------------------------------------------------------')
print("")

year = int(input("Choose a year: "))
schedule = fastf1.get_event_schedule(year).loc[:, ['RoundNumber', 'EventName', 'Country']]

print('--------------------------------------------------------------------------------------------------------')
print(schedule)
print('--------------------------------------------------------------------------------------------------------')

eventtype = int(input("Which event would you like to view(use RoundNumber): "))
sessiontype = input("Which session (eg: FP1, Q, R): ").upper()

Session = fastf1.get_session(year, eventtype, sessiontype)
Session.load()
circuit_info = Session.get_circuit_info()

print('--------------------------------------------------------------------------------------------------------')
print(Session)
print('--------------------------------------------------------------------------------------------------------')
if sessiontype == 'Q':
    print(Session.results.loc[:, ['Abbreviation', 'TeamName', 'Q3', 'Q2', 'Q1']])
else:
    print(Session.results.loc[:, ['GridPosition', 'Abbreviation', 'Time']])
print('--------------------------------------------------------------------------------------------------------')

on = True

while on == True:
    mode = input("What would you like to do?" + "\n" + "1: View laptimes of a driver in the session" + "\n" + "2: Compare one or two drivers' laptimes over the session on a graph" + "\n" + "3: View telemetry of a driver's lap in the session on an animated bar chart" + "\n" + "4: View telemetry of a driver's lap in the session on a graph" + "\n" +"5: Compare 1 or 2 drivers' laps in the session on an animated map" + "\n" +"6: Compare 1 or 2 drivers' laps in the session on a graph" + "\n" + "q to quit" + "\n: ")
    if mode == "1":
        viewlaptimes()
    elif mode == "2":
        comparelaptimesgraph()
    elif mode == "3":
        viewtelebar()
    elif mode == "4":
        viewlaptelegraph()
    elif mode == "5":
        comparelaptimemap()
    elif mode == "6":
        comparelapspeedgraph()
    elif mode == "q":
        on = False
    else:
        print("Invalid input, please try again.")