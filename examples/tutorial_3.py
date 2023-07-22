from timberas.geometry import TimberSection, ShapeType
from timberas.material import TimberMaterial
from timberas.member import (
    BoardMember,
    ApplicationCategory,
    EffectiveLengthFactor,
    DurationFactorStrength,
)


#########################
# Tensile Capacity
# Example 3.3, pg 188
# Timber Design Handbook
#########################
TM = TimberMaterial
TS = TimberSection

print("")
print("EG3.3(a) Design tensile capacity for permanent action case ")

# create a section and remove bolt holes from section tensile area
sec = TS.from_library("190x35")
sec.A_t = sec.A_g - 2 * 22 * sec.b
print(sec.A_t)

# create a material and update properties from the section size
mat = TM.from_library("MGP10")
mat.update_from_section_size(sec.d)
print(mat.f_t)

# create a member
member = BoardMember(
    sec=sec, mat=mat, application_cat=2, k_1=0.57, high_temp_latitude=False
)

# output
member.report(["k_1", "N_dt"])
print("(ANS: N_dt = 14.5 kN)")

print("")
print("EG3.3(b) Design tensile capacity for wind action case")

# update member load duration factor and output
member.update_k_1(DurationFactorStrength.FIVE_SECONDS)
member.report(["k_1", "N_dt"], with_nomenclature=True, with_clause=True)
print("(ANS: N_dt = 25.4 kN)")

#########################
# Compressive Capacity
# Example 4.1, pg 235
# Timber Design Handbook
#########################

print("")
print("EG4.1(a) Compression Capacity - pinned-pinned ends")

# assume pinned-pinned end fixity
g_13 = EffectiveLengthFactor.PINNED_PINNED

# create member
member_dict = {
    "sec": sec,
    "mat": mat,
    "application_cat": 2,
    "r": 1.0,
    "k_1": 1.0,
    "g_13": g_13,
    "L": 2800,
}
member = BoardMember(**member_dict)
# output
member.report(["g_13", "N_dcx", "N_dcy"])
member.report(["S3", "S4", "k_12_c", "N_dc"])
print("(ANS: S3 = 14.7, S4 = 80, k_12_c = 0.042, N_dc = 3.54 kN)")


# update end fixity - assume as semi-rigid from bolt group
print("\nEG4.1(b) Compression Capacity - bolted ends")
member.g_13 = {
    "x": EffectiveLengthFactor.BOLTED_END_RESTRAINT,
    "y": EffectiveLengthFactor.PINNED_PINNED,
}
# resolve member capacities
member.solve_capacities()
# output
member.report(["g_13", "S3", "N_dcx", "S4", "N_dcy"], with_nomenclature=False)
print("(ANS S3 = 11.1)")


##############################################
# Compressive Capacity with Laterial Restraint
# Example 4.3, pg 255
# Timber Design Handbook
##############################################

print("")
print("EG4.3a Timber Stud Wall Design  - L_ay=1650mm")

# Example 4.3 Stud Wall
member_dict = {
    "sec": TS(d=147, b=47, name="Nominal 150 x 50", shape_type=ShapeType.SINGLE_BOARD),
    "mat": TM.from_library("F7 Unseasoned Softwood"),
    "application_cat": ApplicationCategory.SECONDARY_MEMBER,
    "high_temp_latitude": False,
    "consider_partial_seasoning": True,
    "k_1": 0.57,
    "r": 0,
    "g_13": EffectiveLengthFactor.FRAMING_STUDS,
    "L": 3300,
    "L_a": {"x": None, "y": 1650},
}
member = BoardMember(**member_dict)
member.report(["L_ax", "L_ay", "k_4"])
member.report(["S3", "S4", "k_12_c", "N_dc", "N_dcx", "N_dcy"])
print("ANS: S3 = 20.1, S4 = 35.1, k_12_c = 0.139, N_dc = 7.05 kN")

# b) increase capacity from additional lateral restraint L_ay = 1100 mm
print("\nEG4.3b Timber Stud Wall Design - L_ay=1100mm")
member.L_a = {"x": None, "y": 1100}
member.solve_capacities()
member.report(["L_ax", "L_ay"])
member.report(["N_dcx", "N_dcy", "N_dc"])
print("ANS: N_dcx = 21.3, N_dcy = 15.9")
