import fastf1
import pandas as pd


def load_session(year, round, session_type, lap_data):

    """
    Load a specific session from the FastF1 data for a given year, round, and session type.

    Args:
        year (int): The year of the race.
        round (int): The round number of the race.
        session_type (str): The type of session (e.g., 'R' for race, 'Q' for qualifying).

    Returns:
        fastf1.core.Session: The loaded session object.
    """

    session = fastf1.get_session(year, round, session_type)
    session.load(telemetry=False, laps=lap_data, weather=False)
    return session


def get_driver_laps(session, drivers, start, end):
    """
        Get lap data for specified drivers within a session.

        Args:
            session (fastf1.core.Session): The loaded session object containing lap data.
            drivers (list): A list of driver abbreviations to filter.
            start (int): The starting lap number.
            end (int): The ending lap number.

        Returns:
            pandas.DataFrame: A DataFrame containing lap times for the specified drivers.
        """
    driver_laps = session.laps.pick_drivers(drivers).pick_laps(range(start, end, 1)).reset_index()
    print(driver_laps[['LapNumber', 'LapTime']])

    return driver_laps


def get_cumulative_points(year):

    """
    Retrieve cumulative points for drivers in a specified year.

    Args:
        year (int): The year for which to retrieve cumulative points.

    Returns:
        pandas.DataFrame: A DataFrame with cumulative points for each driver and team.
    """

    results = []
    schedule = fastf1.get_event_schedule(year).iloc[1:]  # Skip the first row
    rounds = schedule['RoundNumber']
    for round in rounds:
        session = load_session(year, round, 'R',lap_data=False)
        temp = session.results[['Abbreviation', 'TeamName', 'Points']].copy()
        temp.loc[:, 'Round'] = round
        results.append(temp)

    results = pd.concat(results).pivot(index=['Abbreviation', 'TeamName'], columns='Round', values='Points')

    points_columns = results.columns
    for round_idx in range(1, len(points_columns)):
        results[points_columns[round_idx]] += results[points_columns[round_idx - 1]]

    return results