# Contributing

Thanks for considering a contribution.

## Useful Contributions

- Improve the scoring model.
- Add new data source connectors.
- Add tests for scoring edge cases.
- Build a simple web or Streamlit dashboard.
- Improve documentation with real-world example datasets.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m iv_clinic_evaluator analyze --input data/sample_clinics.csv --output report.csv
```

Please keep changes focused and include a short explanation of the business signal being added or changed.
