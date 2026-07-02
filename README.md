# IV Therapy Clinic Valuation Evaluator

[![GitHub stars](https://img.shields.io/github/stars/itsgreat2beme/ClinicValuationEvaluator?style=social)](https://github.com/itsgreat2beme/ClinicValuationEvaluator/stargazers)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A small Python CLI for evaluating IV therapy clinic opportunities in a local area. Use it to compare neighborhoods, existing clinics, or possible expansion markets with a simple weighted scoring model.

It can:

- Rank candidate clinics or neighborhoods from a CSV file.
- Score market opportunity using demand, competition, review quality, price, and accessibility signals.
- Export a ranked CSV report.
- Optionally fetch nearby clinics from Google Places if you provide an API key.

If this helps your clinic research, please star the repo so other builders can find it.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m iv_clinic_evaluator analyze \
  --input data/sample_clinics.csv \
  --output report.csv
```

Example output:

| Rank | Clinic | Area | Opportunity Score |
| --- | --- | --- | --- |
| 1 | Suburban Hydration Studio | North Suburbs | 80.32 |
| 2 | Athlete Recovery Clinic | Westside | 75.72 |
| 3 | Budget Hydration Clinic | Eastside | 68.27 |

## CSV Format

Required columns:

```text
name,area,population,median_income,wellness_interest,competitor_count,avg_rating,review_count,avg_price,parking_score,transit_score
```

Column notes:

- `wellness_interest`: 0-100 estimate of local interest in wellness, beauty, fitness, or recovery services.
- `competitor_count`: nearby IV therapy or med spa competitors.
- `parking_score`: 0-100.
- `transit_score`: 0-100.
- `avg_price`: average IV drip/session price in local currency.

## Optional Google Places Fetch

Set `GOOGLE_PLACES_API_KEY`, then run:

```bash
export GOOGLE_PLACES_API_KEY="your-key"

python -m iv_clinic_evaluator fetch-places \
  --area "Austin, TX" \
  --output data/austin_places.csv
```

The fetched file contains place-level fields. Add local demographic and pricing fields before running `analyze`.

## Scoring

Higher scores indicate stronger clinic opportunity.

The default formula rewards:

- Higher local population and income.
- Higher wellness interest.
- Better ratings and review volume.
- Easier parking and transit.
- Lower direct competition.
- Prices that are not far outside the local median.

This is a directional business-screening tool, not medical, legal, or financial advice.

## Good GitHub Topics

Add these topics on GitHub to help people discover the project:

```text
healthcare, clinic, valuation, market-analysis, python, small-business, location-analysis, iv-therapy
```

## Share Copy

Short post you can use on LinkedIn, X, Reddit, or founder communities:

```text
I built a small open-source Python tool for evaluating IV therapy clinic opportunities by area. It ranks locations using demand, competition, reviews, pricing, and accessibility signals.

Repo: https://github.com/itsgreat2beme/ClinicValuationEvaluator
```

## Contributing

Ideas, bug reports, and pull requests are welcome. Useful next improvements include:

- More data source connectors.
- A Streamlit dashboard.
- Census or local demographic imports.
- Exportable charts for investor or operator reports.
