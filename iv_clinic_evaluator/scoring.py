from __future__ import annotations

from dataclasses import dataclass
from statistics import median


@dataclass(frozen=True)
class ClinicRecord:
    name: str
    area: str
    population: float
    median_income: float
    wellness_interest: float
    competitor_count: float
    avg_rating: float
    review_count: float
    avg_price: float
    parking_score: float
    transit_score: float


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def normalize(value: float, minimum: float, maximum: float) -> float:
    if maximum <= minimum:
        return 50.0
    return clamp(((value - minimum) / (maximum - minimum)) * 100)


def score_records(records: list[ClinicRecord]) -> list[dict[str, float | str]]:
    if not records:
        return []

    populations = [item.population for item in records]
    incomes = [item.median_income for item in records]
    reviews = [item.review_count for item in records]
    competitors = [item.competitor_count for item in records]
    prices = [item.avg_price for item in records]
    median_price = median(prices)

    scored: list[dict[str, float | str]] = []
    for item in records:
        demand = (
            normalize(item.population, min(populations), max(populations)) * 0.35
            + normalize(item.median_income, min(incomes), max(incomes)) * 0.25
            + clamp(item.wellness_interest) * 0.40
        )
        reputation = clamp((item.avg_rating / 5) * 70 + normalize(item.review_count, min(reviews), max(reviews)) * 0.30)
        access = clamp(item.parking_score * 0.55 + item.transit_score * 0.45)
        competition = 100 - normalize(item.competitor_count, min(competitors), max(competitors))
        price_fit = 100 - clamp(abs(item.avg_price - median_price) / max(median_price, 1) * 100)

        opportunity_score = clamp(
            demand * 0.34
            + competition * 0.24
            + reputation * 0.18
            + access * 0.14
            + price_fit * 0.10
        )

        scored.append(
            {
                "name": item.name,
                "area": item.area,
                "opportunity_score": round(opportunity_score, 2),
                "demand_score": round(demand, 2),
                "competition_score": round(competition, 2),
                "reputation_score": round(reputation, 2),
                "access_score": round(access, 2),
                "price_fit_score": round(price_fit, 2),
            }
        )

    return sorted(scored, key=lambda row: float(row["opportunity_score"]), reverse=True)
