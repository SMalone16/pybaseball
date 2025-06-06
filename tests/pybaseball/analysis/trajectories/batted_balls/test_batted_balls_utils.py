from math import sqrt
from numpy import linalg
import pytest

from pybaseball.analysis.trajectories.utils import unit_vector, spin_components


@pytest.mark.parametrize(
    "spin, spin_angle, launch_angle, launch_direction_angle, expected",
    [
        # no spin should yield zero components
        (0, 1, 1, 1, (0, 0, 0)),
        # typical backspin dominated case
        (
            2000,
            30,
            20,
            0,
            (
                181.37993642342178,
                -35.816265655054956,
                98.40438113645162,
            ),
        ),
        # non-zero launch direction with mild spin angle
        (
            1500,
            10,
            45,
            60,
            (
                60.64318699343772,
                -143.61200729546908,
                19.287463144967436,
            ),
        ),
        # negative launch and spin angles
        (
            1500,
            -45,
            -10,
            -30,
            (
                105.83496883462354,
                38.832603668881674,
                -109.38463908060042,
            ),
        ),
        # sidespin only
        (
            3000,
            90,
            0,
            45,
            (
                0.0,
                -0.0,
                314.1592653589793,
            ),
        ),
    ],
)
def test_spin_components(
    spin, spin_angle, launch_angle, launch_direction_angle, expected
):
    wx, wy, wz = spin_components(spin, spin_angle, launch_angle, launch_direction_angle)
    for a, b in zip((wx, wy, wz), (expected)):
        assert a == pytest.approx(b)


@pytest.mark.parametrize(
    "elevation_angle, azimuthal_angle",
    [(1, 1), (2, 2), (2.71828, 3.14159), (-10, 10), (1e3, 1e-3)],
)
def test_unit_vector(elevation_angle, azimuthal_angle):
    velocity_unit_vector = unit_vector(elevation_angle, azimuthal_angle)
    assert linalg.norm(velocity_unit_vector) == pytest.approx(1)
    assert velocity_unit_vector.shape[0] == 3
