""" Datetime DataSource - add hour and year features """
from dataclasses import dataclass
from numbers import Number
from typing import List, Tuple

import pandas as pd
import numpy as np

from nowcasting_dataset.data_sources.data_source import DataSource
from nowcasting_dataset.data_sources.general.general_model import General
from nowcasting_dataset.utils import to_numpy


@dataclass
class GeneralDataSource(DataSource):
    """Add metadata to the batch"""

    object_at_center: str = "GSP"

    def __post_init__(self):
        """Post init"""
        super().__post_init__()

    def get_example(
        self, t0_dt: pd.Timestamp, x_meters_center: Number, y_meters_center: Number
    ) -> General:
        """
        Get example data

        Args:
            t0_dt: list of timestamps
            x_meters_center: x center of patches - not needed
            y_meters_center: y center of patches - not needed

        Returns: batch data of datetime features

        """
        return General(
            t0_dt=to_numpy(t0_dt),  #: Shape: [batch_size,]
            x_meters_center=np.array(x_meters_center),
            y_meters_center=np.array(y_meters_center),
            object_at_center=self.object_at_center,
        )

    def get_locations_for_batch(
        self, t0_datetimes: pd.DatetimeIndex
    ) -> Tuple[List[Number], List[Number]]:
        """This method is not needed for GeneralDataSource"""
        raise NotImplementedError()

    def datetime_index(self) -> pd.DatetimeIndex:
        """This method is not needed for GeneralDataSource"""
        raise NotImplementedError()
