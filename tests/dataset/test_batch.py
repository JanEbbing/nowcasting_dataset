from nowcasting_dataset.data_sources.gsp.gsp_model import GSP
import numpy as np

from nowcasting_dataset.dataset.batch import Batch, GSP
from nowcasting_dataset.dataset.validate import FakeDataset
import torch
from nowcasting_dataset.config.model import Configuration

import xarray as xr


def test_model():

    _ = Batch.fake()


def test_model_to_numpy():

    f = Batch.fake()

    f.change_type_to_numpy()

    assert type(f.gsp) == GSP


def test_model_split():

    f = Batch.fake()

    data = f.split()

    assert len(data) == f.batch_size
    assert type(data[0].gsp) == GSP


def test_model_to_xr_dataset(configuration):

    f = Batch.fake(configuration=configuration)
    f_xr = f.batch_to_dataset()

    assert type(f_xr) == xr.Dataset


def test_model_from_xr_dataset():

    f = Batch.fake()

    f_xr = f.batch_to_dataset()

    _ = Batch.load_batch_from_dataset(xr_dataset=f_xr)


def test_model_from_xr_dataset_to_numpy():

    f = Batch.fake()

    f_xr = f.batch_to_dataset()
    fs = Batch.load_batch_from_dataset(xr_dataset=f_xr)
    # check they are the same
    fs.change_type_to_numpy()
    f.gsp.to_numpy()
    assert f.gsp.gsp_yield.shape == fs.gsp.gsp_yield.shape
    assert (f.gsp.gsp_yield[0].astype(np.float32) == fs.gsp.gsp_yield[0]).all()
    assert (f.gsp.gsp_yield.astype(np.float32) == fs.gsp.gsp_yield).all()


def test_fake_dataset():
    train = torch.utils.data.DataLoader(FakeDataset(configuration=Configuration()), batch_size=None)
    i = iter(train)
    x = next(i)

    x = Batch(**x)
    # IT WORKS
    assert type(x.satellite.sat_data) == torch.Tensor