from visualization import racepace_plot, plot_cumulative_points
from data_processing import get_driver_laps, get_cumulative_points, load_session, get_position_changes
import fastf1.plotting  # Import the plotting module


def main():

    """
    Main function to execute the analysis of F1 race data.

    Loads session data, retrieves driver lap times, and plots race pace comparison and cumulative points.
    """

    # Setup Matplotlib settings
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)

    # Load in the session
    session = load_session(2024, 'Singapore', 'R',True)

    # Plot race pace

    #racepace_plot(session, ['LEC','PIA'], 1, 80)

    #points_results = get_cumulative_points(2023)
    #unique_teams = points_results.index.get_level_values('TeamName').unique()
    #plot_cumulative_points(points_results, unique_teams)

    get_position_changes(session,['LEC','PIA'])


if __name__ == "__main__":
    main()