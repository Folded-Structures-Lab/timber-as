

#import material
from timberas.material import import_material_library, TimberMaterial

#import material from the default library
MATERIAL_LIBRARY = import_material_library()
MGP12 = TimberMaterial.from_library('MGP12',MATERIAL_LIBRARY)
print(MGP12)

#default library is also used if none is provided otherwise
F8 = TimberMaterial.from_library('F8')
print(F8)



#make stud
from timberas.geometry import TimberSection, SectionTypes
stud_dict = {'name': '1/90x45', 'sec_type': SectionTypes.SINGLE_BOARD, 'n': 1, 'b': 45, 'd': 90}
stud = TimberSection(**stud_dict)
print(stud)

from timberas.member import BoardMember

#g_13 = EffectiveLengthFactor.PinnedPinned

## EXAMPLE 2.11, Capacity Factor, pg ...
MGP10 = TimberMaterial.from_library('MGP10')
tm = BoardMember(sec= stud, mat= MGP10, application_cat=1)
print(f'Example 2.11 Solution MGP10 Frames {tm.phi}=0.9')

F17_Hardwood = TimberMaterial.from_library('F17 Seasoned Hardwood')
tm = BoardMember(sec= stud, mat= F17_Hardwood, application_cat=2)
print(f'Example 2.11 Solution Hardwood Trusses {tm.phi}=0.85')

TM = TimberMaterial
TS = TimberSection

## EXAMPLE 3.1 Design Characteristic Tensile Strength, pg 177
tm = BoardMember(sec= TS.from_library('240x45'), mat= TM.from_library('MGP12'))
print(f'Example 3.1 Solution 240 x 45 MGP12 f_t {tm.mat.f_t}=11 MPa')

print(f'Example 3.1 Solution 250 x 50 F14 Unseasoned Hardwood f_t {...}=20.2 MPa')

print(f'Example 3.1 Solution 330 x 65 GL12 f_t {...}=9.6 MPa')
