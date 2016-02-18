import os

from click.testing import CliRunner
import numpy as np
import rasterio

from rio_color.scripts.cli import color, atmos


def equal(r1, r2):
    with rasterio.open(r1) as src1:
        with rasterio.open(r2) as src2:
            return np.array_equal(src1.read(), src2.read())

def test_atmos_cli(tmpdir):
    output = str(tmpdir.join('atmosj1.tif'))
    runner = CliRunner()
    result = runner.invoke(
        atmos,
        [
            '-a', '0.03',
            '-b', '10',
            '-c', '15',
            '-j', '1',
            'tests/rgb8.tif',
            output]
        )
    assert result.exit_code == 0
    assert os.path.exists(output)

    output2 = str(tmpdir.join('atmosj2.tif'))
    runner = CliRunner()
    result = runner.invoke(
        atmos,
        [
            '-a', '0.03',
            '-b', '10',
            '-c', '15',
            '-j', '2',
            'tests/rgb8.tif',
            output2]
        )
    assert result.exit_code == 0
    assert os.path.exists(output2)

    assert equal(output, output2)


def test_color_cli(tmpdir):
    output = str(tmpdir.join('colorj1.tif'))
    runner = CliRunner()
    result = runner.invoke(
        color,
        [
            '-d', 'uint8',
            '-j', '1',
            'tests/rgb8.tif',
            output,
            "gamma 3 1.85",
            "gamma 1,2 1.95",
            "sigmoidal 1,2,3 35 0.13",
            "saturation 115"]
        )
    assert result.exit_code == 0
    assert os.path.exists(output)

    output2 = str(tmpdir.join('colorj2.tif'))
    result = runner.invoke(
        color,
        [
            '-d', 'uint8',
            '-j', '2',
            'tests/rgb8.tif',
            output2,
            "gamma 3 1.85",
            "gamma 1,2 1.95",
            "sigmoidal 1,2,3 35 0.13",
            "saturation 115"]
        )
    assert result.exit_code == 0
    assert os.path.exists(output2)

    assert equal(output, output2)


def test_bad_op(tmpdir):
    output = str(tmpdir.join('noop.tif'))
    runner = CliRunner()
    result = runner.invoke(
        color,
        [
            '-d', 'uint8',
            '-j', '1',
            'tests/rgb8.tif',
            output,
            "foob 115"]
        )
    assert result.exit_code == 2
    assert "foob is not a valid operation" in result.output
    assert not os.path.exists(output)
