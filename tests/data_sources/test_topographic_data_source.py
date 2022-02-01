""" Test for topographic data source """
import numpy as np
import pandas as pd
import pytest

from nowcasting_dataset.data_sources import TopographicDataSource
from nowcasting_dataset.data_sources.metadata.metadata_model import Location


@pytest.mark.parametrize(
    "x, y, left, right, top, bottom",
    [
        (0, 0, -128_000, 126_000, 128_000, -126_000),
        (10, 0, -126_000, 128_000, 128_000, -126_000),
        (30, 0, -126_000, 128_000, 128_000, -126_000),
        (1000, 0, -126_000, 128_000, 128_000, -126_000),
        (0, 1000, -128_000, 126_000, 128_000, -126_000),
        (1000, 1000, -126_000, 128_000, 128_000, -126_000),
        (2000, 2000, -126_000, 128_000, 130_000, -124_000),
        (2000, 1000, -126_000, 128_000, 128_000, -126_000),
        (2001, 2001, -124_000, 130_000, 130_000, -124_000),
    ],
)
def test_get_example_2km(x, y, left, right, top, bottom):
    """Test get examples"""
    size = 2000  # meters
    topo_source = TopographicDataSource(
        filename="tests/data/europe_dem_2km_osgb.tif",
        image_size_pixels=128,
        meters_per_pixel=size,
        forecast_minutes=300,
        history_minutes=10,
    )
    t0_dt = pd.Timestamp("2019-01-01T13:00")
    topo_data = topo_source.get_example(
        Location(t0_datetime_utc=t0_dt, x_center_osgb=x, y_center_osgb=y)
    )
    assert topo_data.data.shape == (128, 128)
    assert len(topo_data.x_osgb) == 128
    assert len(topo_data.y_osgb) == 128
    assert not np.isnan(topo_data.data).any()
    # Topo x and y coords are not exactly set on the edges, but the center of the pixels
    assert np.isclose(left, topo_data.x_osgb.values[0], atol=size)
    assert np.isclose(right, topo_data.x_osgb.values[-1], atol=size)
    assert np.isclose(top, topo_data.y_osgb.values[0], atol=size)
    assert np.isclose(bottom, topo_data.y_osgb.values[-1], atol=size)


@pytest.mark.parametrize(
    "x, y, left, right, top, bottom",
    [
        (0, 0, -128_000, 126_000, 128_000, -126_000),
        (10, 0, -126_000, 128_000, 128_000, -126_000),
        (30, 0, -126_000, 128_000, 128_000, -126_000),
        (1000, 0, -126_000, 128_000, 128_000, -126_000),
        (0, 1000, -128_000, 126_000, 128_000, -126_000),
        (1000, 1000, -126_000, 128_000, 128_000, -126_000),
        (2000, 2000, -126_000, 128_000, 130_000, -124_000),
        (2000, 1000, -126_000, 128_000, 128_000, -126_000),
        (2001, 2001, -124_000, 130_000, 130_000, -124_000),
    ],
)
def test_get_batch_2km(x, y, left, right, top, bottom):
    """Test get batches"""

    batch_size = 4

    size = 2000  # meters
    topo_source = TopographicDataSource(
        filename="tests/data/europe_dem_2km_osgb.tif",
        image_size_pixels=128,
        meters_per_pixel=size,
        forecast_minutes=300,
        history_minutes=10,
    )
    x = np.array([x] * batch_size)
    y = np.array([y] * batch_size)
    t0_datetimes = pd.date_range("2021-01-01", freq="5T", periods=batch_size) + pd.Timedelta("30T")

    locations = []
    for i in range(batch_size):
        locations.append(
            Location(t0_datetime_utc=t0_datetimes[i], x_center_osgb=x[i], y_center_osgb=y[i])
        )

    topo_data = topo_source.get_batch(locations=locations)
    assert "x_index_index" not in topo_data.dims


@pytest.mark.skip("CD does not have access to GCS")
def test_get_example_gcs():
    """Note this test takes ~5 seconds as the topo data has to be downloaded locally"""

    filename = "gs://solar-pv-nowcasting-data/Topographic/europe_dem_1km_osgb.tif"

    size = 2000  # meters
    topo_source = TopographicDataSource(
        filename=filename,
        image_size_pixels=128,
        meters_per_pixel=size,
        forecast_minutes=300,
        history_minutes=10,
    )
    t0_dt = pd.Timestamp("2019-01-01T13:00")
    _ = topo_source.get_example(t0_datetime_utc=t0_dt, x_center_osgb=0, y_center_osgb=0)
