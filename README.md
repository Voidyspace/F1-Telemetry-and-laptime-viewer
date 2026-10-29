F1 telemetry and laptime viewing tool (By @Voidyspace on github)

This tool can visualise f1 telemetry from any session, in any lap, in various different ways, and can save most of the visualisations to the working directory

List of abilities:

⏺️ View all laps set by a driver over one session: (Cannot be saved)
    ⏺ Puts all the laps set by a driver over the course of a session
    ⏺ States the fastest lap made by that driver
    ⏺ Includes total lap time, and individual sector times, as well as tyre compound and life

⏺️ Compare lap times over a session on a graph:
    ⏺ Up to 2 drivers
    ⏺ Plots all of the set lap times over a session onto a graph. 
    
⏺️ View Throttle/Brake inputs over a lap:
    ⏺ Can be viewed on an animated bar chart:
        ⏺Throttle/Brake inputs, as well as speed are visualised on a moving bar chart
    ⏺ Can be viewed on a graph:
        ⏺Throttle/Brake inputs, as well as speed are visualised on a graph.

⏺️ Compare/View a drivers lap in a session:
    ⏺Up to 2 drivers
    ⏺ Can be viewed on an animated track map:
        ⏺ Drivers, represented as moving points, are visuallised on a track map
    ⏺Can be viewed in a graph:
        ⏺ Drivers' speed(y) and distance(x) are plotted on a graph

(examples in 'Examples' folder)

This tool uses FastF1 library for all of its telemetry data and laptimes

(Note: linux users may have to download tkinter aswell is not installed already.)