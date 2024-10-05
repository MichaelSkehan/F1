import seaborn as sns
import matplotlib.pyplot as plt
import timple.timedelta as tmpldelta


def racepace_plot(session, drivers, start, end):

    """
    Compare the lap times of specified drivers in a session and plot their lap times.

    Args:
        session (fastf1.core.Session): The loaded session object containing lap data.
        drivers (list): A list of driver abbreviations to compare.
        start (int): The starting lap number to consider.
        end (int): The ending lap number to consider.

    Returns:
        None: Displays a scatter plot of lap times for the specified drivers.
    """

    driver_laps = session.laps.pick_drivers(drivers).pick_laps(range(start, end, 1)).reset_index()
    print(driver_laps['LapTime'])

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.lineplot(data=driver_laps, x="LapNumber", y="LapTime", ax=ax, hue="Driver", legend='auto')


    subtitle = "Race Pace Comparison: " + " / ".join(drivers)
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    formatter = tmpldelta.TimedeltaFormatter("%m:%s:%ms")
    ax.yaxis.set_major_formatter(formatter)
    ax.invert_yaxis()
    plt.suptitle(subtitle)
    plt.grid(color='w', which='major', axis='both')
    sns.despine(left=True, bottom=True)
    plt.tight_layout()

    return plt.show()


def plot_cumulative_points(results, unique_teams):

    """
       Plot cumulative points for each driver grouped by their respective teams.

       Args:
           results (pandas.DataFrame): A DataFrame containing cumulative points data.
           unique_teams (pandas.Index): An index of unique team names to plot.

       Returns:
           None: Displays line plots of cumulative points for each driver in their respective teams.
       """


    num_teams = len(unique_teams)
    num_cols = 2
    num_rows = (num_teams + num_cols - 1) // num_cols  # Calculate rows based on number of teams

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(8, 12))

    if num_teams > 1:
        axes = axes.flatten()
    else:
        axes = [axes]

    for i, team in enumerate(unique_teams):
        team_data = results.loc[results.index.get_level_values('TeamName') == team]
        for j in range(len(team_data)):
            ax = axes[i]
            driver_data = team_data.iloc[j]
            rounds = driver_data.index.astype(int)
            points = driver_data.values
            driver_abbr = driver_data.name[0]

            ax.plot(rounds, points, label=driver_abbr)
            ax.set_title(team, fontsize=12)
            ax.set_xlabel('Round')
            ax.set_ylabel('Cumulative Points')
            ax.set_ylim(0, 800)  # Set your desired limits here
            ax.legend()

    if num_teams < len(axes):
        for ax in axes[num_teams:]:
            ax.axis('off')

    plt.tight_layout()
    return plt.show()