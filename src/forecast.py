from dataclasses import dataclass
from datetime import datetime, date
from collections import defaultdict


@dataclass
class ForecastData:
    date_time: datetime
    average_temperature: int
    probability_of_rain: float


@dataclass
class ForecastDay:
    day: date
    data: list[ForecastData]

    def summary(self) -> dict[str, object]:
        morning_t, morning_r, afternoon_t, afternoon_r = [], [], [], []
        all_t = [entry.average_temperature for entry in self.data]

        for e in self.data:
            # collect morning period entries
            if 6 <= e.date_time.hour < 12:
                morning_t.append(e.average_temperature)
                morning_r.append(e.probability_of_rain)
            # collection afternoon period entries
            elif 12 <= e.date_time.hour < 18:
                afternoon_t.append(e.average_temperature)
                afternoon_r.append(e.probability_of_rain)

        return {
            "morning_average_temperature": rounded_average(morning_t),
            "morning_chance_of_rain": rounded_average(morning_r, 2),
            "afternoon_average_temperature": rounded_average(afternoon_t),
            "afternoon_chance_of_rain": rounded_average(afternoon_r, 2),
            "high_temperature": max(all_t),
            "low_temperature": min(all_t),
        }


def summarize_forecast(data):
    grp_day = group_by_day(data)
    summaries = {format_date(fd.day): fd.summary() for fd in grp_day}
    return summaries


def rounded_average(data, round_to=0):
    return (
        round(sum(data) / len(data), round_to) if data else "Insufficient forecast data"
    )


def format_date(day: datetime):
    return day.strftime("%A %B %d").replace(" 0", " ")


def group_by_day(data) -> list[ForecastDay]:
    grp_day: dict[date, list[ForecastData]] = defaultdict(list)
    for e in data:
        entry_time = datetime.fromisoformat(e["date_time"].replace("Z", "+00:00"))
        key = entry_time.date()
        grp_day[key].append(
            ForecastData(
                date_time=entry_time,
                average_temperature=e["average_temperature"],
                probability_of_rain=e["probability_of_rain"],
            )
        )
    return [ForecastDay(day=k, data=v) for k, v in grp_day.items()]
