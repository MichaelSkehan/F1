import seaborn as sns
import matplotlib.pyplot as plt
import timple.timedelta as tmpldelta


def racepace_practice_compare(session, drivers, start, end):
    driver_laps = session.laps.pick_drivers(drivers).pick_laps(range(start, end, 1)).reset_index()
    print(driver_laps['LapTime'])

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.scatterplot(data=driver_laps, x="LapNumber", y="LapTime", ax=ax, hue="Driver", s=80, linewidth=0, legend='auto')

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    formatter = tmpldelta.TimedeltaFormatter("%m:%s:%ms")
    ax.yaxis.set_major_formatter(formatter)
    ax.invert_yaxis()
    plt.suptitle("VER V HAM long run laptimes Bahrain FP2 2024")
    plt.grid(color='w', which='major', axis='both')
    sns.despine(left=True, bottom=True)
    plt.tight_layout()

    return plt.show()


def plot_cumulative_points(results, unique_teams):
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