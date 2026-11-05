# Engineering Notes: Concrete Mix Proportion Calculator

## 1. Purpose

The application estimates ingredient quantities for a specified concrete volume using a **nominal loose-volume proportion** such as 1:2:4 (cement:sand:coarse aggregate). It is intended for learning Python, practicing unit handling, and exploring basic concrete-material quantity estimation.

## 2. Calculation sequence

Let:

- `V` = required wet concrete volume (m³)
- `p` = wastage percentage
- `F` = dry-volume factor
- `Cc`, `Cs`, `Ca` = cement, sand, and coarse aggregate mix parts
- `D = Cc + Cs + Ca` = total mix parts
- `rho_c`, `rho_s`, `rho_a` = assumed loose bulk densities (kg/m³)
- `w/c` = water-cement ratio by mass

### Step A — Include the wastage allowance

`V_batch = V × (1 + p/100)`

### Step B — Estimate combined dry ingredient volume

`V_dry = V_batch × F`

### Step C — Allocate ingredient volumes by proportion

`V_cement = V_dry × Cc/D`

`V_sand = V_dry × Cs/D`

`V_coarse = V_dry × Ca/D`

### Step D — Convert loose volumes into approximate masses

`M_cement = V_cement × rho_c`

`M_sand = V_sand × rho_s`

`M_coarse = V_coarse × rho_a`

### Step E — Estimate water quantity

`M_water = M_cement × (w/c)`

For a first approximation, water density is taken as 1 kg/L, so `water volume (L) ≈ water mass (kg)`.

### Step F — Estimate cement bags

`Cement bags = M_cement / bag mass`

The purchase estimate rounds this value up to the next whole bag.

## 3. Worked example

Inputs:

- Required concrete volume: 1.00 m³
- Nominal loose-volume ratio: 1:2:4
- Wastage: 5%
- Dry-volume factor: 1.54
- Cement / sand / coarse aggregate loose bulk density assumptions: 1,440 / 1,600 / 1,500 kg/m³
- Water-cement ratio: 0.50
- Cement bag mass: 50 kg

Calculations:

- Batch wet volume = 1.00 × 1.05 = 1.05 m³
- Combined dry volume = 1.05 × 1.54 = 1.617 m³
- Total proportion parts = 1 + 2 + 4 = 7
- Cement loose volume = 1.617 × 1/7 = 0.231 m³
- Sand loose volume = 1.617 × 2/7 = 0.462 m³
- Coarse aggregate loose volume = 1.617 × 4/7 = 0.924 m³
- Cement mass = 0.231 × 1,440 = 332.6 kg (approximately)
- Sand mass = 0.462 × 1,600 = 739.2 kg
- Coarse aggregate mass = 0.924 × 1,500 = 1,386.0 kg
- Water = 332.6 × 0.50 = 166.3 L (approximately)
- Cement bags = 332.6/50 = 6.65, so purchase about 7 full bags

Small differences can occur from rounding displayed values.

## 4. Assumptions and limitations

This simplified approach makes several assumptions:

1. The mix ratio is a **loose-volume ratio**, not a mass ratio.
2. The selected dry-volume factor is an approximate conversion factor and must be justified for the materials and method used.
3. The bulk densities are editable placeholders, not universal constants. Actual density depends on material source, grading, moisture, compaction, and measurement method.
4. The water calculation uses cement mass and a specified water-cement ratio. It does not correct for free water in aggregates or water absorbed by dry aggregates.
5. No strength, slump, durability, or compliance result is calculated.
6. No allowance is made for admixtures, entrained/entrapped air, aggregate absorption, particle packing, or measured batch yield.

For structural or production concrete, use the applicable recognised mix-design procedure, measured material properties, trial batches, laboratory tests, and the relevant local standards and engineer's approval.

## 5. Validation plan

- Check that all physical inputs are positive and finite.
- Confirm that ingredient volumes sum to the calculated combined dry volume.
- Confirm that the water mass equals cement mass multiplied by the selected water-cement ratio.
- Confirm that adding 10% wastage scales calculated ingredient quantities by 1.10 when all other inputs remain unchanged.
- Verify example calculations independently with a calculator or spreadsheet.

The included automated tests cover these software checks. They do not validate the empirical suitability of the engineering assumptions.

## 6. Suggested next engineering improvements

- Replace generic density defaults with measured values and source documentation.
- Add wet aggregate moisture content and absorption corrections.
- Add separate fine/coarse aggregate grading and specific gravity inputs.
- Add a measured batch-yield correction based on trial-batch observations.
- Implement a recognised mix-design workflow only after selecting the applicable standard and obtaining the necessary inputs.
