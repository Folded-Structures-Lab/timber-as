
# Sections and Materials

Python code for the following examples are available in the Github repository [example folder](https://github.com/Folded-Structures-Lab/timber-as/tree/main/examples/tutorial_2.py). 

## Define a timber section
*timberas* creates a structural section property using the *TimberSection* class in the *geometry* module. A TimberSection can be imported from a library of 'standard' Australian timber section sizes [(link here)](https://github.com/Folded-Structures-Lab/timber-as/blob/main/src/timberas/data/section_library.csv) using the below code. Section properties can be accessed as attributes of the created section. 
```
from timberas.geometry import TimberSection

# define a section from the section library
section = TimberSection.from_library("2/90x45")
print(section)

# access section properties
print(section.I_x)
print(f"Gross Area for {section.name}: {section.A_g} mm^2")
```

Sections can also be defined directly, with example code shown below.
```
from timberas.geometry import TimberSection, ShapeType

# define a custom section
user_section = TimberSection(
    shape_type=ShapeType.SINGLE_BOARD, 
    b=45, 
    d=90, 
    name="90x45"
)
print(user_section)
print(f"Shape constant {ShapeType.SINGLE_BOARD} = {ShapeType.SINGLE_BOARD.value}")
```
The shape_type attribute defines a particular shape to use for calculating section properties and the ShapeType class contains constants of available shapes.

## Define a timber material

A timber material property is similarly defined using the *TimberMaterial* class in the *material* module. A TimberMaterial can be imported from a library of Australian timber materials [(link here)](https://github.com/Folded-Structures-Lab/timber-as/blob/main/src/timberas/data/material_library.csv), compiled from various tables in AS1720. 

```
from timberas.material import TimberMaterial

#define a material from the material library 
material = TimberMaterial.from_library("F8 Unseasoned Softwood")
print(material)

# access section properties
print(material.f_b)

```

Several material properties in AS1720 are influenced by the timber section size. The *TimberMaterial* *update_from_section_size* method updates a material's properties based on its material type and input section dimensions. For example:
```
#define material
material = TimberMaterial.from_library("MGP10")
print(f"Unmodified material strengths: {material.f_b}, {material.f_t}")

#update material assuming a 240mm deep section
material.update_from_section_size(240)
print(f"Modified material strengths: {material.f_b}, {material.f_t}")
```

## Timber Handbook Examples
The following example is sourced from the *Timber Design Handbook* ([Standards Australia HB 108 - 2013](https://infostore.saiglobal.com/en-us/standards/sa-hb-108-2013-119982_saig_as_as_251451/)), written by Geoffrey Boughton and Keith Crews. This handbook provides detailed guidance and additional information on the design of Australian timber structures. 

>*Example 3.1, Timber Design Handbook (page 177)*
>
> Determine the design characteristic tensile strength for the following members:  
> (a) 240 x 45 mm MGP12  
> (b) 250 x 50 mm unseasoned F14 hardwood  
> (c) 240 x 45 mm GL12  
> (d) 90 x 35 mm MGP10  

Solution using *timberas*: 
```
from timberas.geometry import TimberSection, ShapeType
from timberas.material import TimberMaterial

#EG 3.1(a)
sec = TimberSection.from_library("240x45")
mat = TimberMaterial.from_library("MGP12")
mat.update_from_section_size(sec.d)
print(f"EG3.1(a) 240 x 45 MGP12 f_t = {mat.f_t} (ANS: 11 MPa)")

#EG 3.1(b)
sec = TimberSection(d=250, b=50, shape_type=ShapeType.SINGLE_BOARD)
mat = TimberMaterial.from_library("F14 Unseasoned Hardwood")
mat.update_from_section_size(sec.d)
print(f"EG3.1(b) 250 x 50 F14 Unseasoned Hardwood f_t = {mat.f_t} (ANS: 20.2 MPa)")

#EG 3.1(c)
sec = TimberSection(d=330, b=65, shape_type=ShapeType.SINGLE_BOARD)
mat = TimberMaterial.from_library("GL12")
mat.update_from_section_size(sec.d)
print(f"EG3.1(c) 330 x 65 GL12 f_t = {mat.f_t} (ANS: 9.6 MPa)")

#EG 3.1(d)
sec = TimberSection.from_library("90x35")
mat = TimberMaterial.from_library("MGP10")
mat.update_from_section_size(sec.d)
print(f"EG3.1(d) 90 x 35 MGP10 f_t = {mat.f_t} (ANS: 7.7 MPa)")

```


