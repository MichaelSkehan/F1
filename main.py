from visualization import racepace_plot, plot_cumulative_points
from data_processing import get_driver_laps, get_cumulative_points, load_session
import fastf1.plotting  # Import the plotting module


def main():

    """
    Main function to execute the analysis of F1 race data.

    Loads session data, retrieves driver lap times, and plots race pace comparison and cumulative points.
    """

    # Setup Matplotlib settings
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)

    # Load in the session
    session = load_session(2024, 'Monaco', 'R',True)

    # Plot race pace
    get_driver_laps(session,['VER', 'LEC'],2,80)
    racepace_plot(session, ['VER','LEC'], 2, 80)

    #points_results = get_cumulative_points(2023)
    #unique_teams = points_results.index.get_level_values('TeamName').unique()
    #plot_cumulative_points(points_results, unique_teams)


if __name__ == "__main__":
    main()