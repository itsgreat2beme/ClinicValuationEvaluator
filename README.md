# IV Clinic Evaluator

A small Python CLI for evaluating IV therapy clinic opportunities in a local area.

It can:

- Rank candidate clinics or neighborhoods from a CSV file.
- Score market opportunity using demand, competition, review quality, price, and accessibility signals.
- Export a ranked CSV report.
- Optionally fetch nearby clinics from Google Places if you provide an API key.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m iv_clinic_evaluator analyze \
  --input data/sample_clinics.csv \
  --output report.csv
```

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
