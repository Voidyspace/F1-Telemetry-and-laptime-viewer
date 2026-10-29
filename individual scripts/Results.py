import os
import fastf1

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

eventtype = int(input("Which event would you like to view(use RoundNo): "))
sessiontype = input("Which session (eg: FP1, Q, R): ").upper()

session = fastf1.get_session(year, eventtype, sessiontype)
session.load()
print(session)
print('------------------------------------------------------------------------------------------------------------------')
if sessiontype == 'Q':
    print(session.results.loc[:, ['Abbreviation', 'TeamName', 'Q3']])
else:
    print(session.results.loc[:, ['GridPosition', 'Abbreviation', 'Time']])
print('------------------------------------------------------------------------------------------------------------------')

driver = input("Which driver's laps would you like to view (Use abbreviation): ").upper()

print('------------------------------------------------------------------------------------------------------------------')
print("Fastest lap:", session.laps.pick_drivers(driver).pick_fastest())
print('------------------------------------------------------------------------------------------------------------------')
print(session.laps.pick_drivers(driver).loc[:, ['LapTime', 'Compound', 'TyreLife', 'Deleted', 'Sector1Time', 'Sector2Time', 'Sector3Time']])
print('------------------------------------------------------------------------------------------------------------------')