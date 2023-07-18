"""
This module provides classes and functions to manage timber sections and their geometric properties.

Classes:    
    ShapeType: Enum class defining section type string constants. 

    TimberSection: A class is used to manage timber section attributes. 

    RectangleShape: Represents structural section properties for a rectangular cross-section. 

    TimberShape: An alias for the RectangleShape class.
    
Functions:
    import_section_library(): Returns a DataFrame containing the section library defined
    in timberas/data/section_library.csv

"""

from __future__ import annotations

from importlib.resources import files
from dataclasses import dataclass, field
from math import nan, isnan, floor, log10
from enum import Enum, auto
import pandas as pd


class ShapeType(str, Enum):
    """
    An enumeration of section type string constants. Provides a type-safe way of representing
    different section types.

    Attributes:
        SINGLE_BOARD (str): Represents a section composed of a single board, e.g. 90x35
        MULTI_BOARD (str): Represents a section composed of multiple boards, e.g. 2/90x35
        ROUND (str): Represents a round section (unused)
    """

    # NOTE: can use StrEnum from Python 3.11
    SINGLE_BOARD = "single_board"
    MULTI_BOARD = "multi_board"
    ROUND = "round"


@dataclass(kw_only=True)
class TimberSection:
    """
    Calculates geometric and structural section properties from cross-section parameters. Selects
    shape class from shape_type to calculate: A_g, A_t, A_c, I_x, I_y. Class properties Z_x, Z_y,
    b_tot, and A_s calculated as derived attributes.

    Attributes:
        shape_type (ShapeType | str): The type of the section shape.

        b (float): The breadth of the section.
        d (float): The depth of the section.
        n (int, optional): The number of members in the section. Default = 1.
        name (str, optional): The name of the section. Defaults to an empty string.
        shape (TimberShape): The shape of the section, calculated after initialization.
        A_g (float): The gross area of the section, calculated after shape is solved.
        A_t (float): The tensile area of the section, calculated after shape is solved.
        A_c (float): The compressive area of the section, calculated after shape is solved.
        I_x (float): The moment of inertia about the x-axis, calculated after shape is solved.
        I_y (float): The moment of inertia about the y-axis, calculated by shape if not provided.
        sig_figs (int, optional): Number of significant figures to round calaculated values to.
        Defaults to 4.
    """

    shape_type: ShapeType | str

    b: float
    d: float
    n: int = 1
    name: str = ""

    # b_tot: float = field(init=False)
    A_g: float = nan
    A_t: float = nan
    A_c: float = nan
    I_x: float = nan
    I_y: float = nan

    shape: TimberShape = field(init=False)
    # round values to a number of significant figures
    sig_figs: int = field(repr=False, default=4)

    def __post_init__(self):
        self.solve_shape()

    def solve_shape(self):
        """Sets shape class based on shape_type and recalculates relevant section properties."""
        if self.shape_type in [ShapeType.SINGLE_BOARD, ShapeType.MULTI_BOARD]:
            self.shape = RectangleShape(d=self.d, b=self.b_tot)
        else:
            raise NotImplementedError(
                f"section type: {self.shape_type} has no shape function"
            )

        if self.A_g is nan:
            self.A_g = self.shape.A_g
        if self.A_t is nan:
            self.A_t = self.shape.A_g
        if self.A_c is nan:
            self.A_c = self.shape.A_g
        if self.I_x is nan:
            self.I_x = self.shape.I_x
        if self.I_y is nan:
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
    def from_dict(cls, input_dict: dict, solve_me: bool = True) -> TimberSection:
        """
        Create a TimberSection by directly populating attributes from input dictionary,
        ignoring dictionary keys which aren't class attributes.

        Args:
            input_dict: Defines timber material data to be added, keys corresponding to class
            attribute names will be updated and others will be ignored
            solve_me: If True will run solve_shape() after attributes are added

        Returns:
            TimberSection: The timber section object.
        """

        # Get a list of all class attributes
        valid_keys = cls.__annotations__.keys()
        # Only keep key-value pairs where the key is a valid class attribute
        valid_dict = {k: v for k, v in input_dict.items() if k in valid_keys}
        # Create a new instance using the valid key-value pairs
        new_obj = cls(**valid_dict)
        if solve_me:
            new_obj.solve_shape()
        return new_obj

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
        return cls.from_dict(sec_dict)

    @property
    def b_tot(self) -> float:
        """total width of section containing one or multiple boards, b_tot = n x b"""
        return self.n * self.b

    @property
    def Z_x(self) -> float:
        """Section modulus about x-axis."""
        if self.shape_type in [ShapeType.SINGLE_BOARD, ShapeType.MULTI_BOARD]:
            z_mod = self.b_tot * self.d**2 / 6
        else:
            raise NotImplementedError(
                f"Section Modulus not defined for {self.shape_type}."
            )
        return z_mod

    @property
    def Z_y(self) -> float:
        """Section modulus about y-axis.
        NOTE: Z for block section uses b_tot (n x b), but k12 stability factor uses b.
        """
        raise NotImplementedError
        # if self.shape_type == ShapeType.SINGLE_BOARD:
        #     raise NotImplementedError
        # elif self.shape_type == ShapeType.MULTI_BOARD:
        #     raise NotImplementedError
        # else:
        #     raise NotImplementedError(
        #         f"Section Modulus not defined for {self.shape_type}."
        #     )
        # return z_mod

    @property
    def A_s(self) -> float:
        """shear plane area 3.2.5"""
        return 2 / 3 * self.d * self.b_tot


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
    Class properties A_g, I_x, and I_y calculated as derived attributes.

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
