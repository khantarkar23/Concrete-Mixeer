import math
import pytest

from mix_calculator import MixInputs, calculate_mix


def test_one_cubic_metre_one_two_four_without_wastage():
    inputs = MixInputs(concrete_volume_m3=1.0, wastage_percent=0.0)
    result = calculate_mix(inputs)

    # Dry volume = 1.00 × 1.54 = 1.54 m³; total parts = 7.
    assert result.dry_material_volume_m3 == pytest.approx(1.54)
    assert result.cement_volume_m3 == pytest.approx(1.54 / 7)
    assert result.sand_volume_m3 == pytest.approx(1.54 * 2 / 7)
    assert result.coarse_aggregate_volume_m3 == pytest.approx(1.54 * 4 / 7)
    assert result.cement_mass_kg == pytest.approx((1.54 / 7) * 1440)
    assert result.sand_mass_kg == pytest.approx((1.54 * 2 / 7) * 1600)
    assert result.coarse_aggregate_mass_kg == pytest.approx((1.54 * 4 / 7) * 1500)
    assert result.water_volume_l == pytest.approx(result.cement_mass_kg * 0.5)


def test_wastage_scales_material_quantities():
    without_wastage = calculate_mix(MixInputs(wastage_percent=0.0))
    with_wastage = calculate_mix(MixInputs(wastage_percent=10.0))

    assert with_wastage.cement_mass_kg == pytest.approx(without_wastage.cement_mass_kg * 1.10)
    assert with_wastage.sand_mass_kg == pytest.approx(without_wastage.sand_mass_kg * 1.10)
    assert with_wastage.water_volume_l == pytest.approx(without_wastage.water_volume_l * 1.10)


def test_cement_bags_round_up_to_whole_bags():
    result = calculate_mix(MixInputs(wastage_percent=0.0, cement_bag_mass_kg=50.0))
    assert result.cement_bags_rounded_up == math.ceil(result.cement_mass_kg / 50.0)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"concrete_volume_m3": 0},
        {"cement_parts": 0},
        {"sand_parts": -1},
        {"coarse_aggregate_parts": 0},
        {"dry_volume_factor": 0},
        {"water_cement_ratio": 0},
        {"water_cement_ratio": 1.6},
        {"wastage_percent": -1},
        {"wastage_percent": 101},
        {"cement_bulk_density_kg_m3": 0},
        {"cement_bag_mass_kg": 0},
    ],
)
def test_invalid_inputs_raise_value_error(kwargs):
    with pytest.raises(ValueError):
        calculate_mix(MixInputs(**kwargs))
