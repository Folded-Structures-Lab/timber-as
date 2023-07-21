"""Getting Started Examples"""


############################
# 1. Define a Timber Section
############################

from timberas.geometry import TimberSection, ShapeType

# EG 1A
print("\n Example 1A: Define a timber section from library import")
section = TimberSection.from_library("2/90x45")
print(section)
print(section.I_x)
print(f"Gross Area for {section.name}: {section.A_g} mm^2")

# EG 1B
print("\n Example 1B: Define a custom timber section")
user_section = TimberSection(
    shape_type=ShapeType.SINGLE_BOARD, b=45, d=90, name="90x45"
)
print(user_section)
print(f"Shape constant {ShapeType.SINGLE_BOARD} = {ShapeType.SINGLE_BOARD.value}")

############################
# 2. Define a Timber Material
############################

from timberas.material import TimberMaterial

# EG 2A
print("\n Example 2A: Define a timber material from the material library")
material = TimberMaterial.from_library("F8 Unseasoned Softwood")
print(material)
print(material.f_b)

# EG 2B
print("\n Example 2B: Update material properties from section size")
material = TimberMaterial.from_library("MGP10")
print(f"Unmodified material strengths: {material.f_b}, {material.f_t}")
material.update_from_section_size(240)
print(f"Modified material strengths: {material.f_b}, {material.f_t}")


########################################
# 3 Examples from Timber Design Handbook
# SA HB 108-2013
########################################

# EG 3 Design Characteristic Tensile Strength, pg 177
print("\n Timber Design Handbook EG3.1 Design Characteristic Tensile Strength")

# EG 3.1(1)
sec = TimberSection.from_library("240x45")
mat = TimberMaterial.from_library("MGP12")
mat.update_from_section_size(sec.d)
print(f"EG3.1(a) 240 x 45 MGP12 f_t = {mat.f_t} (ANS: 11 MPa)")

# EG 3.1(b)
sec = TimberSection(d=250, b=50, shape_type=ShapeType.SINGLE_BOARD)
mat = TimberMaterial.from_library("F14 Unseasoned Hardwood")
mat.update_from_section_size(sec.d)
print(f"EG3.1(b) 250 x 50 F14 Unseasoned Hardwood f_t = {mat.f_t} (ANS: 20.2 MPa)")

# EG 3.1(c)
sec = TimberSection(d=330, b=65, shape_type=ShapeType.SINGLE_BOARD)
mat = TimberMaterial.from_library("GL12")
mat.update_from_section_size(sec.d)
print(f"EG3.1(c) 330 x 65 GL12 f_t = {mat.f_t} (ANS: 9.6 MPa)")

# EG 3.1(d)
sec = TimberSection.from_library("90x35")
mat = TimberMaterial.from_library("MGP10")
mat.update_from_section_size(sec.d)
print(f"EG3.1(d) 90 x 35 MGP10 f_t = {mat.f_t} (ANS: 7.7 MPa)")


#########################
# Capacity Factor
# Example 2.11, pg 163
# Timber Design Handbook
#########################

from timberas.member import ApplicationCategory

print("\n Timber Design Handbook  EG2.11 Capacity Factors")

# specify application category as integer 1, 2, or 3
material_a = TimberMaterial.from_library("MGP10")
application_category = 1
phi = material_a.phi(application_category)
print(f"Example 2.11(a) Solution MGP10 Frames phi = {phi} (ANS: 0.9)")

# or, specify application category from ApplicationCategory enum
material_b = TimberMaterial.from_library("F17 Seasoned Hardwood")
application_category = ApplicationCategory.GREATER_THAN_25_SQM
phi = material_b.phi(application_category)
print(f"Example 2.11(b) Solution Hardwood Trusses phi = {phi} (ANS=0.85)")
print(f"Application Category value = {application_category.value}")
