"""Getting Started Examples"""

# A) Define a timber section
from timberas.geometry import TimberSection, SectionType

# from a user input
user_section = TimberSection(
    sec_type=SectionType.SINGLE_BOARD, b=45, d=90, name="90x45"
)
print(user_section)

# access section properties
print(user_section.I_x)
print(f"Gross Area for {user_section.name}: {user_section.A_g} mm^2")

# from the library
section = TimberSection.from_library("2/90x45")
print(section)


# B) Define a timber material
from timberas.material import import_material_library, TimberMaterial

# import material from the default library
MATERIAL_LIBRARY = import_material_library()
MGP12 = TimberMaterial.from_library("MGP12", MATERIAL_LIBRARY)
print(MGP12)

# the default library is also used if none is provided otherwise
F8 = TimberMaterial.from_library("F8 Unseasoned Softwood")
print(F8)


# # define a material
# mat = TM.from_library("MGP12")
# member_dict = {
#     "sec": sec,
#     "mat": mat,
#     "application_cat": 1,
#     "g_13": EffectiveLengthFactor.PINNED_PINNED,
#     "L": 2400,
#     "L_ay": 600,
# }
# member = BoardMember(**member_dict)


# print(f"Default design factors: k_1 = {member.k_1}, r={member.r}, k_6={member.g_13}")
# print(f"EG4.1(a) Design compression capacity N_dc = {member.N_dc} (ANS: 3.54 kN)")
