
# Quick Start

Python code for the following examples are available in the Github repository [examples folder](https://github.com/Folded-Structures-Lab/timber-as/tree/main/examples/tutorial_1.py). 

*timberas* can be used to determine the material properties, section properties, and design capacities for structural members as per Australian Standard AS1720.1:2020 (Timber Structures Part 1: Design Methods).

A typical operation is shown in the below example. Section and material properties are first defined from library import. A structural member is then defined from section, material, and design information. See the following pages for additional information. 

```
from timberas.geometry import TimberSection 
from timberas.material import TimberMaterial 
from timberas.member import BoardMember

#create section and materials
section = TimberSection.from_library("90x45")
material = TimberMaterial.from_library("MGP10")
print(section)
print(material)

# create a structural member
member = BoardMember(sec=section, mat=material, application_cat=1)
print(member)
```