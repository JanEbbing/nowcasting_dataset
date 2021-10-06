from nowcasting_dataset.data_sources.datetime.datetime_model import Datetime
from nowcasting_dataset.data_sources.gsp.gsp_model import GSP
from nowcasting_dataset.data_sources.pv.pv_model import PV
from nowcasting_dataset.data_sources.nwp.nwp_model import NWP
from nowcasting_dataset.data_sources.satellite.satellite_model import Satellite
from nowcasting_dataset.data_sources.sun.sun_model import Sun
from nowcasting_dataset.data_sources.topographic.topographic_model import Topographic


def test_datetime():

    s = Datetime.fake(
        batch_size=4,
        seq_length_5=13,
    )


def test_gsp():

    s = GSP.fake(batch_size=4, seq_length_30=13, n_gsp_per_batch=32)


def test_gsp_pad():

    s = GSP.fake(batch_size=4, seq_length_30=13, n_gsp_per_batch=7).split()[0]
    s.to_numpy()
    s.pad(n_gsp_per_example=32)

    assert s.gsp_yield.shape == (13, 32)


def test_gsp_split():

    s = GSP.fake(batch_size=4, seq_length_30=13, n_gsp_per_batch=32)
    split = s.split()

    assert len(split) == 4
    assert type(split[0]) == GSP
    assert (split[0].gsp_yield == s.gsp_yield[0]).all()


def test_gsp_join():

    s = GSP.fake(batch_size=2, seq_length_30=13, n_gsp_per_batch=32).split()

    s: GSP = GSP.create_batch_from_examples(s)

    assert s.batch_size == 2
    assert len(s.gsp_yield.shape) == 3
    assert s.gsp_yield.shape[0] == 2
    assert s.gsp_yield.shape[1] == 13
    assert s.gsp_yield.shape[2] == 32


def test_nwp():

    s = NWP.fake(batch_size=4, seq_length_5=13, nwp_image_size_pixels=64, number_nwp_channels=8)


def test_nwp_split():

    s = NWP.fake(batch_size=4, seq_length_5=13, nwp_image_size_pixels=64, number_nwp_channels=8)
    s = s.split()


def test_pv():

    s = PV.fake(batch_size=4, seq_length_5=13, n_pv_systems_per_batch=128)


def test_nwp_pad():

    s = PV.fake(batch_size=4, seq_length_5=13, n_pv_systems_per_batch=37).split()[0]
    s.to_numpy()
    s.pad(n_pv_systems_per_example=128)

    assert s.pv_yield.shape == (13, 128)


def test_satellite():

    s = Satellite.fake(
        batch_size=4, seq_length_5=13, satellite_image_size_pixels=64, number_sat_channels=7
    )

    assert s.sat_x_coords is not None


def test_sun():

    s = Sun.fake(
        batch_size=4,
        seq_length_5=13,
    )


def test_topo():

    s = Topographic.fake(
        batch_size=4,
        satellite_image_size_pixels=64,
    )
