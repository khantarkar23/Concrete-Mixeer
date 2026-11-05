# Concrete Mix Proportion Calculator

A beginner-friendly Python + Streamlit portfolio project for estimating material quantities in a **nominal volumetric concrete mix**.

## What it calculates

- Cement, sand, and coarse aggregate loose volumes.
- Approximate masses using editable bulk-density assumptions.
- Water quantity from the selected water-cement ratio (by mass).
- Approximate cement bags, including a rounded-up purchasing quantity.
- A material mass chart and downloadable CSV/JSON calculation records.

## Important engineering scope

This is an **educational quantity estimator**, not a code-compliant concrete mix-design method. It does not calculate or guarantee compressive strength. It does not account for aggregate grading, specific gravity, absorption, free moisture, air content, admixtures, trial-batch yield, exposure class, workability requirements, or local design standards. Do not use it as the sole basis for construction or structural concrete.

The default 1:2:4 ratio, dry-volume factor, and material bulk densities are illustrative assumptions. Replace them with values appropriate to your materials and local practice, and clearly state the source of each assumption in any submitted report.

## Quick start on macOS

1. Extract this project folder.
2. Open the folder in Finder.
3. Double-click `run_project_mac.command`.
4. The script creates a local virtual environment, installs dependencies, and launches the app in your browser.

Alternatively, from Terminal in this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Run the tests

```bash
source .venv/bin/activate
python -m pytest -q
```

## Example calculation

For a nominal 1:2:4 cement:sand:coarse aggregate loose-volume ratio, 1.00 m³ target concrete volume, 5% wastage, 1.54 dry-volume factor, assumed bulk densities of 1,440 / 1,600 / 1,500 kg/m³, a 0.50 water-cement ratio, and 50 kg cement bags:

- Wet batch volume after wastage: 1.05 m³
- Estimated combined dry ingredient volume: 1.617 m³
- Cement: approximately 332.6 kg (about 6.65 bags; purchase 7 full bags)
- Sand: approximately 739.2 kg (0.462 m³)
- Coarse aggregate: approximately 1,386.0 kg (0.924 m³)
- Water: approximately 166.3 L

These values are only the output of the stated assumptions. They are not a recommended structural concrete mix.

## Project structure

```text
concrete_mix_proportion_calculator/
├── app.py
├── mix_calculator.py
├── requirements.txt
├── run_project_mac.command
├── ENGINEERING_NOTES.md
├── README.md
└── tests/
    └── test_mix_calculator.py
```

## Portfolio extensions

1. Add a calculator using a recognised local or international mix-design procedure, after studying the relevant standard.
2. Add aggregate moisture and absorption corrections using measured material properties.
3. Add cost estimation using current supplier quotations.
4. Add an experimental trial-batch worksheet and compare calculated against measured yield and slump.
5. Add compressive-strength test results at 7 and 28 days; do not infer strength from the nominal ratio alone.

## Suggested portfolio description

**Concrete Mix Proportion Calculator — Python Application**  
Developed an interactive Python application to estimate concrete ingredient quantities from a nominal volumetric mix ratio, target batch volume, wastage allowance, and water-cement ratio. Implemented validation, editable material assumptions, quantity tables, visualisation, downloadable calculation records, and automated unit tests. Documented engineering assumptions and limitations, including the distinction between nominal quantity estimation and laboratory-validated mix design.
