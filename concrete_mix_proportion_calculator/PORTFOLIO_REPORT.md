# Concrete Mix Proportion Calculator

**Project type:** Civil Engineering + Python application  
**Tools:** Python, Streamlit, Pandas, Matplotlib, Pytest  
**Level:** Beginner to intermediate

## Abstract

This project develops an interactive Python application that estimates the quantities of cement, fine aggregate, coarse aggregate, and water required for a user-specified concrete batch. The user enters the target concrete volume, a nominal loose-volume mix proportion, water-cement ratio, wastage allowance, and material-property assumptions. The application calculates estimated ingredient volumes and masses, estimates the number of cement bags, presents the results in a table and chart, and exports the calculation record.

The project is designed to demonstrate how programming can support basic construction quantity estimation. It is deliberately described as a nominal mix quantity estimator rather than a structural concrete mix-design tool.

## Engineering problem

Construction planning requires estimates of the materials needed for a concrete batch. Manual calculations are straightforward for simple proportions, but repeated calculations across different volumes and assumptions can be time-consuming and prone to arithmetic or unit errors. A small, transparent calculator can make the calculation sequence repeatable and allow users to test the influence of volume, wastage, mix ratio, and water-cement ratio.

## Objectives

1. Convert a target wet concrete volume into an estimated combined dry ingredient volume.
2. Allocate the dry ingredient volume according to a cement:sand:coarse aggregate proportion.
3. Convert ingredient volumes to approximate masses using assumed loose bulk densities.
4. Estimate mixing water from the selected water-cement ratio by mass.
5. Estimate cement bag quantities and provide downloadable results.
6. Validate the calculation implementation using automated software tests.

## Methodology

The program applies the following sequence:

1. Apply the user's wastage allowance to the target concrete volume.
2. Multiply the resulting wet batch volume by an editable dry-volume factor.
3. Divide the combined dry volume by the sum of the selected mix parts.
4. Allocate cement, sand, and coarse aggregate volumes by their respective parts.
5. Multiply each loose ingredient volume by its assumed bulk density to estimate mass.
6. Multiply cement mass by the water-cement ratio to estimate water mass; approximate water volume using 1 kg ≈ 1 L.
7. Display calculated quantities and export a CSV table and JSON record of inputs and outputs.

The calculation formulas and limitations are documented in `ENGINEERING_NOTES.md`.

## Demonstration case

The following example illustrates the program's default assumptions with a 1:2:4 nominal loose-volume ratio:

| Parameter | Demonstration value |
|---|---:|
| Required concrete volume | 1.00 m³ |
| Cement:sand:coarse aggregate | 1:2:4 |
| Wastage allowance | 5% |
| Dry-volume factor | 1.54 |
| Cement bulk density assumption | 1,440 kg/m³ |
| Sand bulk density assumption | 1,600 kg/m³ |
| Coarse aggregate bulk density assumption | 1,500 kg/m³ |
| Water-cement ratio | 0.50 |
| Cement bag mass | 50 kg |

Calculated example quantities:

| Material | Approximate volume | Approximate mass / quantity |
|---|---:|---:|
| Cement | 0.231 m³ | 332.6 kg (6.65 bags; purchase estimate 7 bags) |
| Sand | 0.462 m³ | 739.2 kg |
| Coarse aggregate | 0.924 m³ | 1,386.0 kg |
| Water | 0.166 m³ | 166.3 L |

These are outputs from the assumptions listed above, not a recommended mix recipe or proof of strength or durability.

## Software validation

The project includes automated tests for:

- The calculation sequence in the 1:2:4 demonstration case.
- Proportional scaling of ingredient quantities when wastage changes.
- Rounding cement bag purchases up to whole bags.
- Rejection of invalid zero, negative, non-finite, and out-of-range inputs.

Run the tests with:

```bash
python -m pytest -q
```

The tests verify the implemented arithmetic and input validation; they do not validate material assumptions or establish concrete performance.

## Limitations and responsible engineering use

This application does not implement a recognised code-based concrete mix-design procedure. It does not predict compressive strength or guarantee workability, durability, or structural adequacy. The calculation does not account for aggregate grading, specific gravity, moisture content, absorption, free surface water, air content, admixtures, trial-batch yield, exposure conditions, or local code requirements.

The dry-volume factor and bulk densities are editable illustrative assumptions. Real values should be measured or obtained from reliable material test data and documented. Water must be adjusted for actual aggregate moisture and absorption. Any concrete intended for construction should be designed using the applicable recognised procedure, verified material properties, trial batches, and laboratory testing under the relevant local standards and professional engineering review.

## Learning outcomes

This project demonstrates:

- Translating a civil-engineering quantity-estimation workflow into an algorithm.
- Applying consistent engineering units and input validation.
- Separating calculation logic from the user interface.
- Building an interactive interface with Streamlit.
- Presenting engineering results with tables and charts.
- Exporting results in reusable formats.
- Writing automated tests and documenting limitations.

## Future improvements

1. Add measured aggregate moisture and absorption corrections.
2. Add aggregate specific gravity and grading inputs.
3. Add a measured trial-batch yield correction.
4. Add supplier-based material cost estimation.
5. Implement a recognised mix-design workflow after choosing and documenting the applicable standard and required test inputs.
6. Compare calculated quantities with a laboratory trial batch and record measured slump, density, yield, and compressive strength.

## Suggested CV / portfolio entry

**Concrete Mix Proportion Calculator | Python, Streamlit**  
Designed and developed an interactive Python application to estimate concrete ingredient quantities from nominal volumetric proportions, batch volume, wastage allowance, and water-cement ratio. Implemented engineering calculations, input validation, editable material assumptions, visual reporting, downloadable outputs, and automated tests. Documented the limitations of nominal quantity estimation and the need for material testing and code-compliant mix design before construction use.
