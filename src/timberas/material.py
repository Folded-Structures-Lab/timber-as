"""
This module provides the `TimberMaterial` class, a data model for representing timber materials based on AS1720. 

The `TimberMaterial` class supports the creation of timber material objects with attributes like name, grade, whether it's seasoned, and various material properties. It also includes methods to retrieve the capacity factor for a given application category, update material properties based on specific rules (e.g. deep sections), and create a `TimberMaterial` instance from a dictionary or a pandas DataFrame material library.

An in-memory material library (`MATERIAL_LIBRARY`), loaded from a CSV file, is also provided for easy and quick lookup of common timber materials.

Classes:
    TimberMaterial: Represents a timber material based on AS1720.

Variables:
    MATERIAL_LIBRARY (pd.DataFrame): In-memory material library loaded from a CSV file.
"""

import pandas as pd
from importlib.resources import files
from dataclasses import dataclass, field
#from timberas.utils import ApplicationCategory


@dataclass(kw_only = True)
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

    def phi(self, application_cat: int):
        """Returns the appropriate capacity factor for the given application category.

        Args:
            application_cat: The application category.

        Returns:
            float: The capacity factor for the given application category.

        Raises:
            ValueError: If the application category is not recognized.
        """
        match application_cat:
            case 1: return self.phi_1
            case 2: return self.phi_2
            case 3: return self.phi_3
            case _: raise ValueError(f'Application Category {application_cat} not recognised.')
                 
    def update_f_t(self, d: float):
        """Updates the f_t property for large Glulam sections according to AS1720.1 Table 7.1 note.

        Args:
            d: The dimension of the timber section.
        """
        
        if self.grade_type == 'GL' and d > 150:
            self.f_t = round(self.f_t * (150/d)**0.167, 3)
        
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
    def from_library(cls, name: str, library: pd.DataFrame | None = None ):
        """Creates a TimberMaterial object from a material library (DataFrame).

        Args:
            name: The name of the timber material to lookup in the library (in 'name' column)
            library (pd.DataFrame, optional): The DataFrame containing the library of timber materials.
                If not provided, the default library `MATERIAL_LIBRARY` is used.

        Returns:
            TimberMaterial: The timber material object.
        """
        if library is None:
            library = MATERIAL_LIBRARY
        material = library.loc[library['name'] == name]
        mat_dict = material.to_dict(orient='records')[0]
        return cls.from_dict(**mat_dict)
        



MATERIAL_LIBRARY= pd.read_csv(files('timberas.data').joinpath('material_library.csv'))
'''docstring for MATERIAL LIBRARY'''



def main():   
    print(MATERIAL_LIBRARY)

    MGP10 = TimberMaterial.from_library('MGP10')
    MGP10 = TimberMaterial.from_library('MGP10', MATERIAL_LIBRARY)
    print(MGP10)
    
if __name__ == "__main__":
    main()
