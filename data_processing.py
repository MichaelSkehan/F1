import fastf1
import pandas as pd


def load_session(year, round, session_type):
    session = fastf1.get_session(year, round, session_type)
    session.load(telemetry=False, laps=True, weather=False)
    return session


def get_driver_laps(session, drivers, start, end):
    return session.laps.pick_drivers(drivers).pick_laps(range(start, end, 1)).reset_index()


def get_cumulative_points(year):
    results = []
    schedule = fastf1.get_event_schedule(year).iloc[1:]  # Skip the first row
    rounds = schedule['RoundNumber']
    for round in rounds:
        session = load_session(year, round, 'R')
        temp = session.results[['Abbreviation', 'TeamName', 'Points']].copy()
        temp.loc[:, 'Round'] = round
        results.append(temp)

    results = pd.concat(results).pivot(index=['Abbreviation', 'TeamName'], columns='Round', values='Points')

    points_columns = results.columns
    for round_idx in range(1, len(points_columns)):
        results[points_columns[round_idx]] += results[points_columns[round_idx - 1]]

    return results