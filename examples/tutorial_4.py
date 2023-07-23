"""Example timberas code for evaluation of member bending and shear capacities"""

from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import (
    BoardMember,
    GlulamMember,
    ApplicationCategory,
    DurationFactorStrength,
    RestraintEdge,
)


#########################
# Bending Capacity
# Example 5.1, pg 333
# Timber Design Handbook
#########################

print("")
print("EG5.1 Design of a Formwork Bearer")
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
    "L_a": {"x": None, "y": 450},
    "restraint_edge": RestraintEdge.COMPRESSION,
}
member = BoardMember(**member_dict)
member.report(["S1", "k_12_bend", "M_d", "L_CLR", "CLR"])
print("(ANS: k_12_bend = 1.0, M_d = 9.75kNm)")
# S1 = 8.87 in Timber Handbook Example as it doesn't use L<L_CLR check first


############################
# Bending and Shear Capacity
# Example 5.6, pg 401
# Timber Design Handbook
############################

print("")
print("EG5.6 Design of a floor beam for the strength limit state")
print("a) Permanent and short-term (5 day) load case")
sec = TS.from_library("GL395x85")
mat = TM.from_library("GL12")
mat.update_from_section_size(sec.d)
member_dict = {
    "sec": sec,
    "mat": mat,
    "application_cat": ApplicationCategory.PRIMARY_MEMBER,
    "k_1": DurationFactorStrength.FIVE_DAYS,
    "r": 0.25,
    "L": 4000,
    "L_a": {"x": None, "y": 450},
    "restraint_edge": RestraintEdge.COMPRESSION,
}
member = GlulamMember(**member_dict)
member.report(["S1", "k_12_bend", "M_d", "V_d"])
print("(ANS: k_12_bend = 1.0, M_d = 41.7 kNm, V_d = 71.6 kN)")
# S1 = 6.39 in Timber Handbook Example as it doesn't use L<L_CLR check first

print("b) Permanent load case")
member.update_k_1(DurationFactorStrength.FIFTY_YEARS)
member.report(["M_d", "V_d"])
print("(ANS: M_d = 25.3 kNm, V_d = 43.5 kN)")
