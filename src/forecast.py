from datetime import datetime
from collections import defaultdict


class ForecastDay:
    def __init__(self, date, morning_temp, morning_rain, afternoon_temp, afternoon_rain, high_temp, low_temp):
        self.date = date
        self.morning_temp = morning_temp
        self.morning_rain = morning_rain
        self.afternoon_temp = afternoon_temp
        self.afternoon_rain = afternoon_rain
        self.high_temp = high_temp
        self.low_temp = low_temp


def summarize_forecast(data):
    grp_day = defaultdict(list)
    summaries = {}

    # Group entries by day
    grp_day = group_by_day(data)

    # Process each day
    for day, entries in grp_day.items():
        morning_t, morning_r, afternoon_t, afternoon_r = [], [], [], []
        all_t = [entry["average_temperature"] for entry in entries]

        for e in entries:
            entry_time = datetime.fromisoformat(e["date_time"].replace('Z', '+00:00'))
            # collect morning period entries
            if 6 <= entry_time.hour < 12:
                morning_t.append(e["average_temperature"])
                morning_r.append(e["probability_of_rain"])
            # collection afternoon period entries
            elif 12 <= entry_time.hour < 18:
                afternoon_t.append(e["average_temperature"])
                afternoon_r.append(e["probability_of_rain"])

        summary = {
            # if no morning data, report insufficient data
            "morning_average_temperature": rounded_average(morning_t),
            "morning_chance_of_rain": rounded_average(morning_r, 2),
            # if no afternoon data, report insufficient data
            "afternoon_average_temperature": rounded_average(afternoon_t),
            "afternoon_chance_of_rain": rounded_average(afternoon_r, 2),
            "high_temperature": max(all_t),
            "low_temperature": min(all_t)
        }

        # format reader-friendly date
        day_name = format_date(day)

        summaries[day_name] = summary

    return summaries


def rounded_average(data, round_to=0):
    return round(sum(data) / len(data), round_to) if data else "Insufficient forecast data"


def format_date(day):
    return day.strftime("%A %B %d").replace(" 0", " ")


def group_by_day(data):
    grp_day = defaultdict(list)
    for e in data:
        entry_time = datetime.fromisoformat(e["date_time"].replace('Z', '+00:00'))
        key = entry_time.date()
        grp_day[key].append(e)
    return grp_day
