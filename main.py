import fastf1
import seaborn as sns
from matplotlib import pyplot as plt
import fastf1.plotting
import timple.timedelta as tmpldelta
import pandas as pd

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

def racepace_practice_compare(date, track, sessn, drivers, start,end):
    session = fastf1.get_session(date, track, sessn)
    session.load(telemetry=False, laps=False, weather=False)
    
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
        session.load(telemetry=False, laps=False, weather=False)

        temp = session.results[['Abbreviation','TeamName', 'Points']].copy()
        temp.loc[:, 'Round'] = round  
        results.append(temp)

    results = pd.concat(results)
    results = results.pivot(index=['Abbreviation','TeamName'], columns='Round', values='Points')

    points_columns = results.columns

    for round_idx in range(1, len(points_columns)):
        # Calculate cumulative sum for each round
        results[points_columns[round_idx]] += results[points_columns[round_idx - 1]]

    # Get unique team names
    unique_teams = results.index.get_level_values('TeamName').unique()

    # Define the number of rows and columns for subplots
    num_teams = len(unique_teams)
    num_cols = 2  
    num_rows = 5

    # Create subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(8, 12))

    # Flatten axes if necessary
    if num_teams > 1:
      axes = axes.flatten()
    else:
        axes = [axes]

    # Plot cumulative sum for each team
    for i, team in enumerate(unique_teams):
        team_data = results.loc[results.index.get_level_values('TeamName') == team]
        for j in range(len(team_data)):
            ax = axes[i]
            driver_data = team_data.iloc[j]
            rounds = driver_data.index.astype(int)  # Convert rounds to integers
            points = driver_data.values  # Exclude the first value which is the driver name
            driver_abbr = driver_data.name[0]

            ax.plot(rounds, points, label=driver_abbr)
            ax.set_title(team, fontsize=14)
            ax.set_xlabel('Round')
            ax.set_ylabel('Cumulative Points')

            ax.set_ylim(0, 800)  # Set your desired limits here
            ax.legend()

    # Hide extra subplots if needed
    if num_teams < len(axes):
        for ax in axes[num_teams:]:
            ax.axis('off')

    # Adjust layout and display plot
    plt.tight_layout()

    return plt.show()

points_cumulative(2023)
