# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 13:37:31 2022

@author: uqjgatta
"""
from __future__ import annotations

from importlib.resources import files
from dataclasses import dataclass, field
from math import nan, isnan, floor, log10
from enum import Enum

import pandas as pd


class SectionTypes(str, Enum):
    """TODO"""

    # NOTE: can use StrEnum from Python 3.11
    SINGLE_BOARD = "single_board"
    MULTI_BOARD = "multi_board"
    ROUND = "round"


def import_section_library() -> pd.DataFrame:
    """
    Imports a section library from a CSV file.

    The CSV file should be located at 'timberas.data/section_library.csv'.

    Returns:
        pd.DataFrame: A DataFrame containing the contents of the section library CSV file.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    file_name: str = str(files("timberas.data").joinpath("section_library.csv"))
    return pd.read_csv(file_name)


@dataclass
class RectangleShape():
    '''Structural section properties for a rectangular cross-section.'''
    d: float = nan
    b: float = nan

    @property
    def A_g(self) -> float:
        '''Gross area'''
        return self.d*self.b

    @property
    def I_x(self) -> float:
        '''Moment of inertia - major axis'''
        return self.b*self.d**3/12

    @property
    def I_y(self) -> float:
        '''Moment of inertia - minor axis'''
        return self.d*self.b**3/12

    # def I_w(self) -> float:
    #     '''Warping constant - NOT IMPLEMENTED'''
    #     I_w = 0
    #     return I_w
    # def J(params: dict) -> float:
    #     '''Torsion constant - NOT IMPLEMENTED'''
    #     #J = 0
    #     a = max(params.d, params.b) #long side
    #     b = min(params.d, params.b) #short side
    #     J = a * b**3 * (1/3 - 0.21 * b / a * (1 - b**4 / (12*a**4)))
    #     return J


TimberShape = RectangleShape




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
    # S_x: float = nan
    # S_y: float = nan
    #Z_x: float = nan
    #Z_y: float = nan
    #r_x: float = nan
    #r_y: float = nan
    # I_w: float = nan
    # J: float = nan

    # x_c: float = 0
    # y_c: float = 0

    shape: TimberShape = field(init=False)
    # round values to a number of significant figures
    sig_figs: int = field(repr=False, default=4)

    def __post_init__(self):
        if self.sec_type != "":
            self.solve_shape()

    def solve_shape(self):
        """TODO"""
        if self.sec_type == SectionTypes.SINGLE_BOARD:
            self.b_tot = self.n * self.b
            self.shape = RectangleShape(d = self.d, b = self.b_tot)
        else:
            raise NotImplementedError(
                f"section type: {self.sec_type} has no shape function"
            )

        self.A_g = self.shape.A_g
        self.A_t = self.shape.A_g
        self.A_c = self.shape.A_g
        self.I_x = self.shape.I_x
        self.I_y = self.shape.I_y
        # self.Z_x = self.shape.Z_x
        # self.S_x = shape_fn.S_x(self)
        # self.S_y = shape_fn.S_y(self)
        # self.J = shape_fn.J(self)
        # self.I_w = shape_fn.I_w(self)

        #self.Z_y = self._Z_y()
        #self.r_x = self._r_x()
        #self.r_y = self._r_y()

        # round to sig figs
        if self.sig_figs:
            for key, val in list(self.__dict__.items()):
                if isinstance(val, (float, int)) and (not isnan(val)) and (val != 0):
                    setattr(
                        self, key, round(val, self.sig_figs - int(floor(log10(abs(val)))) - 1)
                    )


    @classmethod
    def from_dict(cls, **kwargs):
        '''Create a TimberSection by directly populating attributes from input dictionary.
         Ignoring dictionary keys which aren't class attributes. Resolves the section if 
         section properties aren't created by '''
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
        '''Section modulus about x-axis.
        NOTE: Z for block section uses b_tot (n x b), but k12 stability factor uses b.'''
        if self.sec_type == SectionTypes.SINGLE_BOARD:
            z_mod = self.d * self.b_tot**2 / 6
        elif self.sec_type == SectionTypes.MULTI_BOARD:
            z_mod = self.d * self.b_tot**2 / 6
        else:
            raise NotImplementedError(
                f"Section Modulus not defined for {self.sec_type}."
            )
        return z_mod
