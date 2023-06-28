"""TODO"""

from __future__ import annotations

from importlib.resources import files
from dataclasses import dataclass, field
from math import nan, isnan, floor, log10
from enum import Enum

import pandas as pd


class SectionType(str, Enum):
    """
    An enumeration of section type string constants.

    This Enum class is used to provide a type-safe way of representing different section types.

    Attributes:
        SINGLE_BOARD (str): Represents a section composed of a single board, e.g. 90x35
        MULTI_BOARD (str): Represents a section composed of multiple boards, e.g. 2/90x35
        ROUND (str): Represents a round section (unused)
    """

    # NOTE: can use StrEnum from Python 3.11
    SINGLE_BOARD = "single_board"
    MULTI_BOARD = "multi_board"
    ROUND = "round"


def import_section_library() -> pd.DataFrame:
    """
    Imports a section library from a CSV file.

    The CSV file is located at 'timberas.data/section_library.csv'.

    Returns:
        pd.DataFrame: A DataFrame containing the contents of the section library CSV file.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    file_name: str = str(files("timberas.data").joinpath("section_library.csv"))
    return pd.read_csv(file_name)


@dataclass
class RectangleShape:
    """
    Dataclass representing structural section properties for a rectangular cross-section.

    Properties:
        A_g: The gross area of the rectangular section.
        I_x: The moment of inertia along the major axis.
        I_y: The moment of inertia along the minor axis.

    Attributes:
        d (float): The height of the rectangle.
        b (float): The breadth (or width) of the rectangle.
    """

    d: float
    b: float

    @property
    def A_g(self) -> float:
        """Gross area"""
        return self.d * self.b

    @property
    def I_x(self) -> float:
        """Moment of inertia - major axis"""
        return self.b * self.d**3 / 12

    @property
    def I_y(self) -> float:
        """Moment of inertia - minor axis"""
        return self.d * self.b**3 / 12


TimberShape = RectangleShape
"""DOCSTRING TODO"""


@dataclass(kw_only=True)
class TimberSection:
    """TODO"""

    name: str = ""
    section: str = ""
    sec_type: str = ""

    n: int = 1
    b: float = 10
    d: float = nan

    b_tot: float = field(init=False)
    A_g: float = nan
    A_t: float = nan
    A_c: float = nan
    I_x: float = nan
    I_y: float = nan

    shape: TimberShape = field(init=False)
    # round values to a number of significant figures
    sig_figs: int = field(repr=False, default=4)

    def __post_init__(self):
        if self.sec_type != "":
            self.solve_shape()

    def solve_shape(self):
        """TODO"""
        if self.sec_type == SectionType.SINGLE_BOARD:
            self.b_tot = self.n * self.b
            self.shape = RectangleShape(d=self.d, b=self.b_tot)
        else:
            raise NotImplementedError(
                f"section type: {self.sec_type} has no shape function"
            )

        self.A_g = self.shape.A_g
        self.A_t = self.shape.A_g
        self.A_c = self.shape.A_g
        self.I_x = self.shape.I_x
        self.I_y = self.shape.I_y

        # round to sig figs
        if self.sig_figs:
            for key, val in list(self.__dict__.items()):
                if isinstance(val, (float, int)) and (not isnan(val)) and (val != 0):
                    setattr(
                        self,
                        key,
                        round(val, self.sig_figs - int(floor(log10(abs(val)))) - 1),
                    )

    @classmethod
    def from_dict(cls, **kwargs):
        """Create a TimberSection by directly populating attributes from input dictionary.
        Ignoring dictionary keys which aren't class attributes. Resolves the section if
        section properties aren't created by"""
        obj = cls()
        # all_ann = cls.__annotations__
        for key, val in kwargs.items():
            # note - @property items are in hasattr but not in __annotations__)
            if hasattr(obj, key):  # and (k in cls.__annotations__):
                setattr(obj, key, val)

        if isnan(obj.A_g):
            # if section properties aren't created in cls() or by dictionary override, add them here
            obj.solve_shape()
        return obj

    @classmethod
    def from_library(cls, name: str, library: pd.DataFrame | None = None):
        """Creates a TimberSection object from a material library (DataFrame).

        Args:
            name: The name of the timber material to lookup in the library (in 'name' column)
            library (pd.DataFrame, optional): DataFrame containing a library of timber materials.
                If not provided, the default section library is used from import_section_library.

        Returns:
            TimberMaterial: The timber material object.
        """
        if library is None:
            library = import_section_library()
        section = library.loc[library["name"] == name]
        sec_dict = section.to_dict(orient="records")[0]
        return cls.from_dict(**sec_dict)

    @property
    def Z_x(self) -> float:
        """Section modulus about x-axis."""
        if self.sec_type == SectionType.SINGLE_BOARD:
            z_mod = self.d * self.b_tot**2 / 6
        elif self.sec_type == SectionType.MULTI_BOARD:
            z_mod = self.d * self.b_tot**2 / 6
        else:
            raise NotImplementedError(
                f"Section Modulus not defined for {self.sec_type}."
            )
        return z_mod

    @property
    def Z_y(self) -> float:
        """Section modulus about y-axis.
        NOTE: Z for block section uses b_tot (n x b), but k12 stability factor uses b.
        """
        raise NotImplementedError
        # if self.sec_type == SectionType.SINGLE_BOARD:
        #     raise NotImplementedError
        # elif self.sec_type == SectionType.MULTI_BOARD:
        #     raise NotImplementedError
        # else:
        #     raise NotImplementedError(
        #         f"Section Modulus not defined for {self.sec_type}."
        #     )
        # return z_mod
