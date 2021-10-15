""" Pydantic extension of xarray dataset """
import xarray as xr
from typing import Any


class PydanticXArrayDataSet(xr.Dataset):
    """Pydantic Xarray Dataset Class

    Adapted from https://pydantic-docs.helpmanual.io/usage/types/#classes-with-__get_validators__

    """

    _expected_dimensions = ()  # Subclasses should set this.

    __slots__ = []

    @classmethod
    def __get_validators__(cls):
        """Get validators"""
        yield cls.validate_dims

    @classmethod
    def validate(cls, v: Any) -> Any:
        """Do validation"""
        v = cls.validate_dims(v)
        v = cls.validate_coords(v)
        return v
        # TODO: How to call multiple validation functions?

    @classmethod
    def validate_dims(cls, v: Any) -> Any:
        """Validate the dims"""
        assert all(
            dim.replace("_index", "") in cls._expected_dimensions
            for dim in v.dims
            if dim != "example"
        ), (
            f"{cls.__name__}.dims is wrong! "
            f"{cls.__name__}.dims is {v.dims}. "
            f"But we expected {cls._expected_dimensions}. Note that '_index' is removed, and 'example' is ignored"
        )
        return v

    @classmethod
    def validate_coords(cls, v: Any) -> Any:
        """Validate teh coords"""
        for dim in cls._expected_dimensions:
            coord = v.coords[dim]
            assert len(coord) > 0, f"{dim} is empty in {cls.__name__}!"
        return v
