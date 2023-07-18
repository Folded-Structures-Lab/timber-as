# import material
from timberas.member import ApplicationCategory
from timberas.member import EffectiveLengthFactor
from timberas.member import BoardMember
from timberas.geometry import TimberSection, SectionType
from timberas.material import import_material_library, TimberMaterial


# import material from the default library
MATERIAL_LIBRARY = import_material_library()
MGP12 = TimberMaterial.from_library("MGP12", MATERIAL_LIBRARY)
print(MGP12)

# default library is also used if none is provided otherwise
F8 = TimberMaterial.from_library("F8 Unseasoned Softwood")
print(F8)


# make stud
stud_dict = {
    "name": "1/90x45",
    "sec_type": SectionType.SINGLE_BOARD,
    "n": 1,
    "b": 45,
    "d": 90,
}
stud = TimberSection(**stud_dict)
print(stud)


# EXAMPLE 2.11, Capacity Factor, pg ...
MGP10 = TimberMaterial.from_library("MGP10")
tm = BoardMember(sec=stud, mat=MGP10, application_cat=1)

print("\n EG2.11 Capacity Factors")
print(f"Example 2.11 Solution MGP10 Frames {tm.phi}=0.9")

F17_Hardwood = TimberMaterial.from_library("F17 Seasoned Hardwood")
tm = BoardMember(sec=stud, mat=F17_Hardwood, application_cat=2)

print(f"Example 2.11 Solution Hardwood Trusses {tm.phi}=0.85")

TM = TimberMaterial
TS = TimberSection

# EXAMPLE 3.1 Design Characteristic Tensile Strength, pg 177
sec = TS.from_library("240x45")
mat = TM.from_library("MGP12")
mat.update_from_section_size(sec.d)

print("\n EG3.1 Design Characteristic Tensile Strength")
print(f"EG3.1(a) 240 x 45 MGP12 f_t = {mat.f_t} (ANS: 11 MPa)")

sec = TS(d=250, b=50, sec_type=SectionType.SINGLE_BOARD)
mat = TM.from_library("F14 Unseasoned Hardwood")
mat.update_from_section_size(sec.d)

print(f"EG3.1(b) 250 x 50 F14 Unseasoned Hardwood f_t = {mat.f_t} (ANS: 20.2 MPa)")

sec = TS(d=330, b=65, sec_type=SectionType.SINGLE_BOARD)
mat = TM.from_library("GL12")
mat.update_from_section_size(sec.d)
print(f"EG3.1(c) 330 x 65 GL12 f_t = {mat.f_t} (ANS: 9.6 MPa)")

sec = TS.from_library("90x35")
mat = TM.from_library("MGP10")
mat.update_from_section_size(sec.d)
print(f"EG3.1(d) 90 x 35 MGP10 f_t = {mat.f_t} (ANS: 7.7 MPa)")

# EXAMPLE 3.3 Tensile Capacity
sec = TS.from_library("190x35")
sec.A_t = sec.A_g - 2 * 22 * sec.b  # remove bolt holes
mat = TM.from_library("MGP10")
mat.update_from_section_size(sec.d)
member = BoardMember(sec=sec, mat=mat, application_cat=2, high_temp_latitude=False)

print("\n EG3.3 Tensile Capacity")
print(
    f"EG3.3(a) Design tensile capacity for wind action case\
        (k_1 = {member.k_1}), N_dt = {member.N_dt} (ANS: 25.4 kN)"
)

member.update_k_1(0.57)
print(
    f"EG3.3(b) Design tensile capacity for wind action case\
        (k_1 = {member.k_1}), N_dt = {member.N_dt} (ANS: 14.5 kN)"
)

# EXAMPLE 4.1 Compression Capacity
g_13 = EffectiveLengthFactor.PINNED_PINNED
member_dict = {
    "sec": sec,
    "mat": mat,
    "application_cat": 2,
    "r": 1.0,
    "g_13": g_13,
    "L": 2800,
    "L_ay": 2800,
}
member = BoardMember(**member_dict)

print("\n EG4.1 Compression Capacity")
print(f"EG4.1(a): k_1 = {member.k_1}, r={member.r}, g_13={member.g_13}")
print(f"EG4.1(a) Slenderness factor major axis buckling  S3 = {member.S3} (ANS: 14.7)")
print(f"EG4.1(a) Slenderness factor minor axis buckling S4 = {member.S4} (ANS: 80)")
print(f"EG4.1(a) Stability factor k12 = {member.k_12_c} (ANS: 0.042)")
print(f"EG4.1(a) Design compression capacity N_dc = {member.N_dc} (ANS: 3.54 kN)")


member_dict["g_13"] = EffectiveLengthFactor.BOLTED_END_RESTRAINT
member = BoardMember(**member_dict)

print(f"EG4.1(b): k_1 = {member.k_1}, r={member.r}, g_13={member.g_13}")
print(f"EG4.1(a) Slenderness factor major axis buckling  S3 = {member.S3} (ANS: 11.1)")


# Example 4.3 Stud Wall
mat = TM.from_library("F7 Unseasoned Softwood")
member_dict = {
    "sec": TS(d=147, b=47, name="147x47", sec_type=SectionType.SINGLE_BOARD),
    "mat": mat,
    "application_cat": ApplicationCategory.SECONDARY_MEMBER,
    "high_temp_latitude": False,
    "consider_partial_seasoning": True,
    "k_1": 0.57,
    "r": 0,
    "g_13": EffectiveLengthFactor.FRAMING_STUDS,
    "L": 3300,
    "L_ay": 1650,
}
member = BoardMember(**member_dict)

print("\n EG4.3 Timber Stud Wall Design")
print(f"EG4.3(a) Slenderness factor major axis buckling  S3 = {member.S3} (ANS: 20.1)")
print(f"EG4.3(a) Slenderness factor minor axis buckling S4 = {member.S4} (ANS: 35.1)")
print(f"EG4.3(a) Stability factor k12 = {member.k_12_c} (ANS: 0.139)")
print(f"EG4.3(a) Design compression capacity N_dc = {member.N_dc} (ANS: 7.05 kN)")

# Example 4.4 Stud Wall Design Change
member_dict["L_ay"] = 1100
member = BoardMember(**member_dict)

print(
    "\n EG4.4 Timber Stud Wall Modification - increase capacity from \
      additional lateral restraint L_ay = 1100 mm"
)
print(
    f"EG4.4  Check design compression capacity for major axis buckling \
        N_cx = {member.N_cx} (ANS: 21.3 kN)"
)
print(
    f"EG4.4  Check design compression capacity for minor axis bukcling \
        N_cy = {member.N_cy} (ANS: 15.9 kN)"
)


# Example 5.1 Design capacity of a formwork bearer
from timberas.member import DurationFactorStrength, BendingRestraint

sec = TS.from_library("Nominal 250x50")
mat = TM.from_library("F11 Unseasoned Hardwood")
mat.update_from_section_size(sec.d)
member_dict = {
    "sec": sec,
    "mat": mat,
    "application_cat": ApplicationCategory.PRIMARY_MEMBER,
    "k_1": DurationFactorStrength.FIVE_DAYS,
    "r": 0,
    "L": 2700,
    "L_ay": 450,
    "restraint": BendingRestraint.DISCRETE_LATERAL_RESTRAINT_COMPRESSION_EDGE,
}
member = BoardMember(**member_dict)

print(
    "\n EG5.1 Design capacity timber formwork bearer \n"
    f"Slenderness coefficient S1 = {member.S1} (ANS: 8.87) \n"
    f"Stability factor k12 = {member.k_12_bend} (ANS: 1.0) \n"
    f"Design moment capacity M_d = {member.M_d} (ANS: 9.75 kNm) \n"
    f"(Note: k12 = 1 when compression edge lateral restraint < L_CLR, {member.L_ay} < {member.L_CLR})"
)


# Example 5.6 Design of a floor beam for the strength limit state
from timberas.member import GlulamMember

sec = TS.from_library("GL395x85")
mat = TM.from_library("GL12")
# mat.update_from_section_size(sec.d)
member_dict = {
    "sec": sec,
    "mat": mat,
    "application_cat": ApplicationCategory.PRIMARY_MEMBER,
    "k_1": DurationFactorStrength.FIVE_DAYS,
    "r": 0.25,
    "L": 4000,
    "L_ay": 450,
    "restraint": BendingRestraint.DISCRETE_LATERAL_RESTRAINT_COMPRESSION_EDGE,
}
member = BoardMember(**member_dict)

print(
    "\n EG5.6 Design of a floor beam for the strength limit state \n"
    "a) Bending capacity check, critical load case"
    f"Slenderness coefficient S1 = {member.S1} (ANS: 6.39) \n"
    f"Stability factor k12 = {member.k_12_bend} (ANS: 1.0) \n"
    f"Design moment capacity M_d = {member.M_d} (ANS: 41.7 kNm) \n"
    f"(Note: k12 = 1 when compression edge lateral restraint < L_CLR, {member.L_ay} < {member.L_CLR})"
)
print(
    "b) Shear capacity check\n"
    f"Design shear capacity V_d = {member.V_d} (ANS: 71.6 kNm) \n"
)
# SERVICEABILITY CHECK: TODO
# BEARING CAPACITY CHECK: TODO
member.update_k_1(DurationFactorStrength.FIFTY_YEARS)
print(
    "c) Bending capacity check, long-term load case \n"
    f"Design moment capacity M_d = {member.M_d} (ANS: 25.3 kNm) \n"
    f"Design shear capacity V_d = {member.V_d} (ANS: 43.5 kNm) \n"
)
