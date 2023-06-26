"""
This module provides the `TimberMaterial` class, a data model for representing timber materials based on AS1720. 

The `TimberMaterial` class supports the creation of timber material objects with attributes like name, grade, whether it's seasoned, and various material properties. It also includes methods to retrieve the capacity factor for a given application category, update material properties based on specific rules (e.g. deep sections), and create a `TimberMaterial` instance from a dictionary or a pandas DataFrame material library.

The function `import_material_library` reads a material library from a CSV file located at 'timberas.data/material_library.csv' and returns the data as a pandas DataFrame.

Classes:
    TimberMaterial: Represents a timber material based on AS1720.

Functions:
    import_material_library(): Returns a DataFrame containing the contents of the material library CSV file.
"""

import pandas as pd
from importlib.resources import files
from dataclasses import dataclass, field
# from timberas.utils import ApplicationCategory


def import_material_library() -> pd.DataFrame:
    """
    Imports a material library from a CSV file.

    The CSV file should be located at 'timberas.data/material_library.csv'.

    Returns:
        pd.DataFrame: A DataFrame containing the contents of the material library CSV file.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    return pd.read_csv(files('timberas.data').joinpath('material_library.csv'))


@dataclass(kw_only=True)
class TimberMaterial():
    """A class to represent a timber material as defined in AS1720.

    Attributes:
        name: The name of the timber material.
        grade: The grade of the timber material
        seasoned (bool): A boolean indicating whether the timber material is seasoned.
        grade_type: The type of the timber grade, e.g F, MGP, GL. 
        f_b: Material property
        f_t: Material property.
        f_s: Material property.
        f_c: Material property.
        E: Material property.
        G: Material property.
        density: Material property, defaults to 0.
        phi_1: Capacity factor for the material for application category one.
        phi_2: Capacity factor for the material for application category two.
        phi_3: Capacity factor for the material for application category three.
    """
    name: str = ''
    grade: str = ''
    seasoned: bool = True
    grade_type: str = ''
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
        """Returns the appropriate capacity factor for the given application category.

        Args:
            application_cat: The application category.

        Returns:
            float: The capacity factor for the given application category.

        Raises:
            ValueError: If the application category is not recognized.
        """
        p: float = 0
        match application_cat:
            case 1: p = self.phi_1
            case 2: p = self.phi_2
            case 3: p = self.phi_3
            case _: raise ValueError(f'Application Category {application_cat} not recognised.')
        return p

    def update_from_section_size(self, d: float, b: float | None = None) -> None:
        """Updates the f_t property for large Glulam sections according to AS1720.1 Table 7.1 note.

        Args:
            d: The dimension of the timber section.
        """
        if self.grade_type == "MGP" and d > 140:
            match d:
                case 190 | 240 | 290: new_mat = f'{self.name} {d}mm depth'
                case _: raise ValueError(f'Section depth {d} > 140mm - please interpolate material properties for MGP section (table H3.1, Note 4).')
            print(f'Material changed from {self.name} to {new_mat}')
            new_mat = self.from_library(new_mat)
            self.name = new_mat.name
            self.f_b = new_mat.f_b
            self.f_t = new_mat.f_t
            self.f_c = new_mat.f_c
            self.f_s = new_mat.f_s
        elif self.grade_type == 'F':
            if d > 150:
                # Table H.2 Note 2
                original_f_t = self.f_t
                self.f_t = round(self.f_t * (150/d)**0.167, 3)
                print(
                    f'Tensile strength f_t changed from {original_f_t} to {self.f_t} due to section size, Table H.2 Note 2')
            if d > 300:
                # Table H.2 Note 1
                original_f_b = self.f_b
                self.f_b = round(self.f_b * (300/d)**0.167, 3)
                print(
                    f'Bending strength f_b changed from {original_f_b} to {self.f_b} due to section size, Table H.2 Note 1')

        elif self.grade_type == 'GL' and d > 150:
            # Table 7.1 Note
            original_f_t = self.f_t
            self.f_t = round(self.f_t * (150/d)**0.167, 3)
            print(
                f'Tensile strength f_t changed from {original_f_t} to {self.f_t} due to section size, Table 7.1 Note')

    @classmethod
    def from_dict(cls, **kwargs):
        """Creates a TimberMaterial object from a dictionary.

        Args:
            **kwargs: The key-value pairs defining the timber material.

        Returns:
            TimberMaterial: The timber material object.
        """
        o = cls()
        for k, v in kwargs.items():
            setattr(o, k, v)
        return o

    @classmethod
    def from_library(cls, name: str, library: pd.DataFrame | None = None):
        """Creates a TimberMaterial object from a material library (DataFrame).

        Args:
            name: The name of the timber material to lookup in the library (in 'name' column)
            library (pd.DataFrame, optional): The DataFrame containing the library of timber materials.
                If not provided, the default library `MATERIAL_LIBRARY` is used.

        Returns:
            TimberMaterial: The timber material object.
        """
        if library is None:
            library = import_material_library()
        material = library.loc[library['name'] == name]
        mat_dict = material.to_dict(orient='records')[0]
        return cls.from_dict(**mat_dict)


def main():
    MATERIAL_LIBRARY = import_material_library()

    MGP10 = TimberMaterial.from_library('MGP10')
    MGP10 = TimberMaterial.from_library('MGP10', MATERIAL_LIBRARY)
    print(MGP10)


if __name__ == "__main__":
    main()
