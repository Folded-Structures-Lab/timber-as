
# Getting Started

Python code for the following examples is available in the Github repository. 

## A) Define a timber section
*timberas* creates a structural section property using the *TimberSection* class in the *geometry* module. For example, this code creates a rectangular section: 
```
from timberas.geometry import TimberSection, SectionType

#define 

a custom section
user_section = TimberSection(
    sec_type=SectionType.SINGLE_BOARD, d=90, b=45, name="90x45"
)

#output
print(user_section)
```
The section type attribute (sec_type) attribute defines a particular shape to use for calculating section properties, and the SectionType class contains constants of available shapes (e.g. SectionType.SINGLE_BOARD defines a rectangle shape).


Section properties can be accessed as attributes of the created section:
```
print(section.I_x) 
#returns 2734000.0
print(f"Gross Area for {section.name}: {section.A_g} mm^2")
#returns Gross Area for 90x45: 4050 mm^2 
```

*timberas* includes a library of 'standard' Australian timber section sizes (link here). A TimberSection can be imported directly from the library using the section name:
```
section = TimberSection.from_library("2/90x45")
print(section)
```

## B) Define a timber material