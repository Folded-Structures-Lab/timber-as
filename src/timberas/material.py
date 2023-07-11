"""
This module provides classes and functions for creating representing timber materials 
based on AS1720. 

Classes:
    GradeType: Enum class defining material grade string constants. 

    TimberMaterial: Represents a timber material based on AS1720. 

Functions:
    import_material_library(): Returns a DataFrame containing the material library defined
    in timberas/data/material_library.csv
"""
from __future__ import annotations
from importlib.resources import files
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd


class GradeType(str, Enum):
    """
    An enumeration of grade type string constants. Provide a type-safe way of representing
    different grade types.

    Attributes:
        F_GRADE (str): Represents the "F" grade type
        MGP (str): Represents the "MGP" grade type
        GLULAM (str): Represents the "GL" grade type
        A_GRADE (str): Represents the "A" grade type
    """

    F_GRADE = "F"
    MGP = "MGP"
    GLULAM = "GL"
    A_GRADE = "A"


def import_material_library() -> pd.DataFrame:
    """Imports a material library from a CSV file.

    The CSV file is located at 'timberas/data/material_library.csv'.

    Returns:
        pd.DataFrame: A DataFrame containing the contents of the material library CSV file.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    return pd.read_csv(files("timberas.data").joinpath("material_library.csv"))


@dataclass(kw_only=True)
class TimberMaterial:
    """Represents timber material properties as defined in AS1720.

    Attributes:
        name: The name of the timber material.
        grade: The grade of the timber material
        seasoned (bool): A boolean indicating whether the timber material is seasoned.
        grade_type: The type of the timber grade, e.g F, MGP, GL.
        f_b: Material characteristic strength in bending.
        f_t: Material characteristic strength in tension.
        f_s: Material characteristic strength in shear.
        f_c: Material characteristic strength in compression.
        E: Material Modulus of Elasticity.
        G: Material Modulus of Rigidity.
        density: Material density.
        phi_1: Capacity factor for the material for application category one.
        phi_2: Capacity factor for the material for application category two.
        phi_3: Capacity factor for the material for application category three.
    """

    name: str = ""
    grade: str = ""
    seasoned: bool = True
    grade_type: str = ""
    f_b: float = 0
    f_t: float = 0
    f_s: float = 0
    f_c: float = 0
    E: float = 0
    G: float = 0
    density: float = 0
    phi_1: float = field(default=0, repr=False)
    phi_2: float = field(default=0, repr=False)
    phi_3: float = field(default=0, repr=False)

    def phi(self, application_cat: int) -> float:
        """Returns the appropriate capacity factor for the given application
        category.

        Args:
            application_cat: The application category.

        Returns:
            float: The capacity factor for the given application category.

        Raises:
            ValueError: If the application category is not recognized.
        """

        match application_cat:
            case 1:
                return self.phi_1
            case 2:
                return self.phi_2
            case 3:
                return self.phi_3
            case _:
                raise ValueError(
                    f"Application Category {application_cat} not recognised."
                )

    def update_from_section_size(self, d: float, b: float | None = None) -> None:
        """Updates the f_t property for large sections, including:
          f_t, f_b, f_c, f_s for MGP sections with d>140mm (AS1720.1 Table H3.1, Note 4);
          f_b for F-grade sections with d > 300mm (AS1720.1 Table H2.1 Note 1);
          f_t for F-grade sections with d > 150mm (AS1720.1 Table H.2 Note 2);
          f_t for Glulam sections with d > 150mm  (AS1720.1 Table 7.1 Note 1).

        Args:
            d: The depth of the timber section.
            b: The breadth of the timber section (required for A17 material).
        """
        if self.grade_type == GradeType.MGP and d > 140:
            match d:
                case 190 | 240 | 290:
                    new_mat = f"{self.name} {d}mm depth"
                case _:
                    raise ValueError(
                        f"Section depth {d} > 140mm, please interpolate material properties "
                        "for MGP section (table H3.1, Note 4)."
                    )
            print(f"Material changed from {self.name} to {new_mat}")
            new_mat = self.from_library(new_mat)
            self.name = new_mat.name
            self.f_b = new_mat.f_b
            self.f_t = new_mat.f_t
            self.f_c = new_mat.f_c
            self.f_s = new_mat.f_s

        elif self.grade_type == GradeType.F_GRADE:
            if d > 150:
                # Table H.2 Note 2
                original_f_t = self.f_t
                self.f_t = round(self.f_t * (150 / d) ** 0.167, 3)
                print(
                    f"Tensile strength f_t changed from {original_f_t} to {self.f_t}"
                    " due to section size, Table H.2 Note 2"
                )
            if d > 300:
                # Table H.2 Note 1
                original_f_b = self.f_b
                self.f_b = round(self.f_b * (300 / d) ** 0.167, 3)
                print(
                    f"Bending strength f_b changed from {original_f_b} to {self.f_b}"
                    " due to section size, Table H.2 Note 1"
                )
        elif self.grade_type == GradeType.A_GRADE:
            print(f"requires {d} and {b}")
            raise NotImplementedError

        elif self.grade_type == GradeType.GLULAM and d > 150:
            # Table 7.1 Note
            original_f_t = self.f_t
            self.f_t = round(self.f_t * (150 / d) ** 0.167, 3)
            print(
                f"Tensile strength f_t changed from {original_f_t} to {self.f_t}"
                " due to section size, Table 7.1 Note"
            )

    @classmethod
    def from_dict(cls, input_dict: dict) -> TimberMaterial:
        """Create a TimberMaterial by directly populating attributes from input dictionary,
        ignoring dictionary keys which aren't class attributes.

        Args:
            input_dict: Key-value pairs to define the timber material, keys corresponding to class
            attribute names will be updated

        Returns:
            TimberMaterial: The timber material object.
        """

        # Get a list of all class attributes
        valid_keys = cls.__annotations__.keys()
        # Only keep key-value pairs where the key is a valid class attribute
        valid_dict = {k: v for k, v in input_dict.items() if k in valid_keys}
        # Create a new instance using the valid key-value pairs
        return cls(**valid_dict)

    @classmethod
    def from_library(cls, name: str, library: pd.DataFrame | None = None):
        """Creates a TimberMaterial object from a material library (DataFrame).

        Args:
            name: The name of the timber material to lookup in the library (in 'name' column)
            library (pd.DataFrame, optional): The DataFrame of the library of timber materials.
                If not provided, the default library `MATERIAL_LIBRARY` is used.

        Returns:
            TimberMaterial: The timber material object.
        """
        if library is None:
            library = import_material_library()
        material = library.loc[library["name"] == name]
        mat_dict = material.to_dict(orient="records")[0]
        return cls.from_dict(mat_dict)


def main():
    """Main Script"""
    material_library = import_material_library()
    mgp10 = TimberMaterial.from_library("MGP10")
    mgp10 = TimberMaterial.from_library("MGP10", material_library)
    print(mgp10)


if __name__ == "__main__":
    main()
