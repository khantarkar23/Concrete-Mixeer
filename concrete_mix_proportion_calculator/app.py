from __future__ import annotations

import json

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from mix_calculator import MixInputs, calculate_mix, results_table


st.set_page_config(
    page_title="Concrete Mix Proportion Calculator",
    page_icon="🏗️",
    layout="wide",
)

st.title("Concrete Mix Proportion Calculator")
st.caption("An educational batching estimator for nominal volumetric concrete mixes")
st.markdown(
    "Enter a target concrete volume, a cement:sand:coarse aggregate ratio, "
    "and a water-cement ratio. The calculator estimates the material quantities "
    "using editable assumptions."
)

with st.sidebar:
    st.header("1. Concrete batch")
    concrete_volume = st.number_input(
        "Required concrete volume (m³)", min_value=0.01, max_value=10000.0,
        value=1.0, step=0.1, format="%.2f",
    )
    wastage = st.number_input(
        "Wastage allowance (%)", min_value=0.0, max_value=100.0,
        value=5.0, step=1.0,
    )

    st.header("2. Mix proportion")
    st.caption("Loose-volume parts: cement : sand : coarse aggregate")
    ratio_col1, ratio_col2, ratio_col3 = st.columns(3)
    with ratio_col1:
        cement_parts = st.number_input("Cement", min_value=0.01, value=1.0, step=0.5)
    with ratio_col2:
        sand_parts = st.number_input("Sand", min_value=0.01, value=2.0, step=0.5)
    with ratio_col3:
        aggregate_parts = st.number_input("Coarse agg.", min_value=0.01, value=4.0, step=0.5)
    water_cement_ratio = st.number_input(
        "Water-cement ratio (by mass)", min_value=0.01, max_value=1.5,
        value=0.50, step=0.01, format="%.2f",
        help="Water mass divided by cement mass. Actual water must be corrected for aggregate moisture and absorption.",
    )

    st.header("3. Calculation assumptions")
    dry_factor = st.number_input(
        "Dry-volume factor", min_value=1.0, max_value=2.5,
        value=1.54, step=0.01, format="%.2f",
        help="Approximate factor converting wet concrete volume to the combined loose dry ingredient volume. Verify for your materials and method.",
    )
    with st.expander("Material bulk densities and bag size", expanded=False):
        cement_density = st.number_input("Cement bulk density (kg/m³)", min_value=500.0, max_value=2500.0, value=1440.0, step=10.0)
        sand_density = st.number_input("Sand bulk density (kg/m³)", min_value=500.0, max_value=2500.0, value=1600.0, step=10.0)
        aggregate_density = st.number_input("Coarse aggregate bulk density (kg/m³)", min_value=500.0, max_value=2500.0, value=1500.0, step=10.0)
        bag_mass = st.number_input("Cement bag mass (kg)", min_value=1.0, max_value=100.0, value=50.0, step=1.0)

inputs = MixInputs(
    concrete_volume_m3=concrete_volume,
    cement_parts=cement_parts,
    sand_parts=sand_parts,
    coarse_aggregate_parts=aggregate_parts,
    water_cement_ratio=water_cement_ratio,
    dry_volume_factor=dry_factor,
    wastage_percent=wastage,
    cement_bulk_density_kg_m3=cement_density,
    sand_bulk_density_kg_m3=sand_density,
    coarse_aggregate_bulk_density_kg_m3=aggregate_density,
    cement_bag_mass_kg=bag_mass,
)

try:
    results = calculate_mix(inputs)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.subheader("Estimated material quantities")
metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Cement", f"{results.cement_mass_kg:,.1f} kg", f"{results.cement_bags:.2f} bags")
metric2.metric("Sand", f"{results.sand_mass_kg:,.1f} kg", f"{results.sand_volume_m3:.3f} m³")
metric3.metric("Coarse aggregate", f"{results.coarse_aggregate_mass_kg:,.1f} kg", f"{results.coarse_aggregate_volume_m3:.3f} m³")
metric4.metric("Water", f"{results.water_volume_l:,.1f} L", f"w/c = {results.water_cement_ratio:.2f}")

left, right = st.columns([1.25, 1])
with left:
    st.markdown("#### Batch quantity table")
    df = pd.DataFrame(results_table(results))
    st.dataframe(
        df.style.format({"Volume (m³)": "{:.3f}", "Approx. mass (kg)": "{:,.1f}"}),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        f"Buy approximately **{results.cement_bags_rounded_up} full cement bags** "
        f"({bag_mass:.0f} kg per bag). The calculated cement requirement is "
        f"{results.cement_mass_kg:.1f} kg."
    )

with right:
    st.markdown("#### Material mass comparison")
    chart_data = pd.Series(
        {
            "Cement": results.cement_mass_kg,
            "Sand": results.sand_mass_kg,
            "Coarse aggregate": results.coarse_aggregate_mass_kg,
            "Water": results.water_mass_kg,
        }
    )
    fig, ax = plt.subplots(figsize=(7, 4.2))
    chart_data.plot(kind="bar", ax=ax)
    ax.set_ylabel("Approximate mass (kg)")
    ax.set_xlabel("")
    ax.set_title("Estimated batch material masses")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

with st.expander("Calculation steps and formulas"):
    st.markdown(
        "**Step 1 — Allow for wastage**\n\n"
        "Batch wet volume = required volume × (1 + wastage / 100)\n\n"
        "**Step 2 — Estimate dry ingredient volume**\n\n"
        "Dry volume = batch wet volume × dry-volume factor\n\n"
        "**Step 3 — Split the dry volume by mix parts**\n\n"
        "Ingredient volume = dry volume × ingredient parts / total parts\n\n"
        "**Step 4 — Convert loose volume to approximate mass**\n\n"
        "Ingredient mass = ingredient volume × assumed bulk density\n\n"
        "**Step 5 — Estimate mixing water**\n\n"
        "Water mass = cement mass × water-cement ratio\n\n"
        "Water volume (L) ≈ water mass (kg)."
    )
    st.write(
        f"For this batch: {results.target_concrete_volume_m3:.3f} m³ required, "
        f"{results.wastage_percent:.1f}% wastage, giving "
        f"{results.batch_concrete_volume_m3:.3f} m³ batch volume. "
        f"The estimated dry ingredient volume is {results.dry_material_volume_m3:.3f} m³ "
        f"across {results.total_mix_parts:g} total parts."
    )

summary = {
    "inputs": inputs.__dict__,
    "results": results.to_dict(),
    "notice": "Educational nominal volumetric estimate; not a code-compliant mix design.",
}
csv = df.to_csv(index=False).encode("utf-8")
json_bytes = json.dumps(summary, indent=2).encode("utf-8")
download1, download2 = st.columns(2)
with download1:
    st.download_button("Download material quantities (CSV)", data=csv, file_name="concrete_material_quantities.csv", mime="text/csv", use_container_width=True)
with download2:
    st.download_button("Download calculation details (JSON)", data=json_bytes, file_name="concrete_mix_calculation.json", mime="application/json", use_container_width=True)

st.divider()
st.subheader("Engineering limitations — read before using")
st.warning(
    "This tool estimates quantities from a user-selected nominal volumetric ratio. "
    "It does NOT determine a structural concrete mix design or guarantee a target strength. "
    "It does not account for aggregate grading, specific gravity, absorption, free moisture, "
    "air content, admixtures, trial-batch yield, exposure class, workability, or local code requirements. "
    "For construction, use a recognised mix-design method, verified material properties, trial mixes, "
    "and laboratory testing under the applicable standard."
)
st.caption("Portfolio project | Python + Streamlit | Educational estimating tool")
