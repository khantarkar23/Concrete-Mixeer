"""Core calculations for a nominal volumetric concrete mix calculator.

This is an educational estimating tool. It is not an ACI/DOE/IS mix-design
procedure and must not be used as the sole basis for structural concrete work.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil, isfinite
from typing import Any


@dataclass(frozen=True)
class MixInputs:
    """User inputs for one concrete batch.

    The cement:sand:coarse aggregate ratio is interpreted as a loose-volume
    ratio. Bulk densities convert those loose volumes to approximate masses.
    """

    concrete_volume_m3: float = 1.0
    cement_parts: float = 1.0
    sand_parts: float = 2.0
    coarse_aggregate_parts: float = 4.0
    water_cement_ratio: float = 0.50
    dry_volume_factor: float = 1.54
    wastage_percent: float = 5.0
    cement_bulk_density_kg_m3: float = 1440.0
    sand_bulk_density_kg_m3: float = 1600.0
    coarse_aggregate_bulk_density_kg_m3: float = 1500.0
    cement_bag_mass_kg: float = 50.0


@dataclass(frozen=True)
class MixResults:
    """Calculated batch quantities and intermediate values."""

    target_concrete_volume_m3: float
    wastage_percent: float
    batch_concrete_volume_m3: float
    dry_material_volume_m3: float
    total_mix_parts: float
    cement_volume_m3: float
    sand_volume_m3: float
    coarse_aggregate_volume_m3: float
    cement_mass_kg: float
    sand_mass_kg: float
    coarse_aggregate_mass_kg: float
    water_cement_ratio: float
    water_mass_kg: float
    water_volume_l: float
    cement_bags: float
    cement_bags_rounded_up: int
    cement_per_target_m3_kg: float
    sand_per_target_m3_kg: float
    coarse_aggregate_per_target_m3_kg: float
    water_per_target_m3_l: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite number greater than zero.")


def calculate_mix(inputs: MixInputs) -> MixResults:
    """Calculate approximate ingredient quantities for a nominal mix.

    Steps:
    1. Increase the specified wet concrete volume by the wastage allowance.
    2. Multiply by the dry-volume factor to estimate loose dry ingredient volume.
    3. Divide that volume according to the volumetric mix parts.
    4. Convert ingredient volumes to approximate masses using bulk densities.
    5. Calculate water from the specified water/cement mass ratio.

    Aggregate moisture, absorption, grading, air content, admixtures, yield
    corrections, and code-specific mix-design requirements are not modelled.
    """

    positive_fields = {
        "Concrete volume": inputs.concrete_volume_m3,
        "Cement parts": inputs.cement_parts,
        "Sand parts": inputs.sand_parts,
        "Coarse aggregate parts": inputs.coarse_aggregate_parts,
        "Dry-volume factor": inputs.dry_volume_factor,
        "Cement bulk density": inputs.cement_bulk_density_kg_m3,
        "Sand bulk density": inputs.sand_bulk_density_kg_m3,
        "Coarse aggregate bulk density": inputs.coarse_aggregate_bulk_density_kg_m3,
        "Cement bag mass": inputs.cement_bag_mass_kg,
    }
    for name, value in positive_fields.items():
        _validate_positive(name, value)

    if not isfinite(inputs.water_cement_ratio) or not 0 < inputs.water_cement_ratio <= 1.5:
        raise ValueError("Water-cement ratio must be greater than 0 and no more than 1.5.")
    if not isfinite(inputs.wastage_percent) or not 0 <= inputs.wastage_percent <= 100:
        raise ValueError("Wastage must be between 0% and 100%.")

    batch_volume = inputs.concrete_volume_m3 * (1.0 + inputs.wastage_percent / 100.0)
    dry_volume = batch_volume * inputs.dry_volume_factor
    total_parts = (
        inputs.cement_parts + inputs.sand_parts + inputs.coarse_aggregate_parts
    )

    cement_volume = dry_volume * inputs.cement_parts / total_parts
    sand_volume = dry_volume * inputs.sand_parts / total_parts
    coarse_volume = dry_volume * inputs.coarse_aggregate_parts / total_parts

    cement_mass = cement_volume * inputs.cement_bulk_density_kg_m3
    sand_mass = sand_volume * inputs.sand_bulk_density_kg_m3
    coarse_mass = coarse_volume * inputs.coarse_aggregate_bulk_density_kg_m3

    water_mass = cement_mass * inputs.water_cement_ratio
    # At ordinary construction temperatures, 1 kg of water is approximately 1 litre.
    water_volume_l = water_mass

    return MixResults(
        target_concrete_volume_m3=inputs.concrete_volume_m3,
        wastage_percent=inputs.wastage_percent,
        batch_concrete_volume_m3=batch_volume,
        dry_material_volume_m3=dry_volume,
        total_mix_parts=total_parts,
        cement_volume_m3=cement_volume,
        sand_volume_m3=sand_volume,
        coarse_aggregate_volume_m3=coarse_volume,
        cement_mass_kg=cement_mass,
        sand_mass_kg=sand_mass,
        coarse_aggregate_mass_kg=coarse_mass,
        water_cement_ratio=inputs.water_cement_ratio,
        water_mass_kg=water_mass,
        water_volume_l=water_volume_l,
        cement_bags=cement_mass / inputs.cement_bag_mass_kg,
        cement_bags_rounded_up=ceil(cement_mass / inputs.cement_bag_mass_kg),
        cement_per_target_m3_kg=cement_mass / inputs.concrete_volume_m3,
        sand_per_target_m3_kg=sand_mass / inputs.concrete_volume_m3,
        coarse_aggregate_per_target_m3_kg=coarse_mass / inputs.concrete_volume_m3,
        water_per_target_m3_l=water_volume_l / inputs.concrete_volume_m3,
    )


def results_table(results: MixResults) -> list[dict[str, str | float]]:
    """Return a UI-friendly list of calculated material quantities."""
    return [
        {
            "Material": "Cement",
            "Volume (m³)": results.cement_volume_m3,
            "Approx. mass (kg)": results.cement_mass_kg,
            "Batching note": f"{results.cement_bags:.2f} bags; buy about {results.cement_bags_rounded_up} full bags",
        },
        {
            "Material": "Sand",
            "Volume (m³)": results.sand_volume_m3,
            "Approx. mass (kg)": results.sand_mass_kg,
            "Batching note": "Loose volume estimate",
        },
        {
            "Material": "Coarse aggregate",
            "Volume (m³)": results.coarse_aggregate_volume_m3,
            "Approx. mass (kg)": results.coarse_aggregate_mass_kg,
            "Batching note": "Loose volume estimate",
        },
        {
            "Material": "Water",
            "Volume (m³)": results.water_volume_l / 1000.0,
            "Approx. mass (kg)": results.water_mass_kg,
            "Batching note": f"Approximately {results.water_volume_l:.1f} litres",
        },
    ]
