import fastf1
import seaborn as sns
from matplotlib import pyplot as plt
import fastf1.plotting
import timple.timedelta as tmpldelta
import pandas as pd

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

def racepace_practice_compare(date, track, sessn, drivers, start,end):
    session = fastf1.get_session(date, track, sessn)
    session.load()
    
    driver_laps = session.laps.pick_drivers(drivers).pick_laps(range(start,end,1)).reset_index()
    print(driver_laps['LapTime'])
    fig, ax = plt.subplots(figsize=(8, 8))

    sns.scatterplot(data=driver_laps,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                hue="Driver",
                s=80,
                linewidth=0,
                legend='auto')
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")

    # manually set the format to force no offset
    formatter = tmpldelta.TimedeltaFormatter("%m:%s:%ms")
    ax.yaxis.set_major_formatter(formatter)

    # The y-axis increases from bottom to top by default
    # Since we are plotting time, it makes sense to invert the axis
    ax.invert_yaxis()
    plt.suptitle("VER V HAM long run laptimes Bahrain FP2 2024")

    # Turn on major grid lines
    plt.grid(color='w', which='major', axis='both')
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
 

    return plt.show()

#racepace_practice_compare(2024,'Bahrain','FP2',['VER','HAM','PER'],10,22)

def points_cumulative(year):
    results = []
    schedule = fastf1.get_event_schedule(year)
    schedule = schedule.iloc[1:]
    rounds = schedule['RoundNumber']
    for round in rounds:
        session = fastf1.get_session(year,round,'R')
        session.load()

        temp = session.results[['Abbreviation','TeamName', 'Points']].copy()
        temp.loc[:, 'Round'] = round  
        results.append(temp)

    results = pd.concat(results)
    results = results.pivot(index='Abbreviation', columns='Round', values='Points')

    return results

points_cumulative(2023)
