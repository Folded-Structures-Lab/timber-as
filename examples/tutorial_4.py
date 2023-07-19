# # Example 5.1 Design capacity of a formwork bearer
# sec = TS.from_library("Nominal 250x50")
# mat = TM.from_library("F11 Unseasoned Hardwood")
# mat.update_from_section_size(sec.d)
# member_dict = {
#     "sec": sec,
#     "mat": mat,
#     "application_cat": ApplicationCategory.PRIMARY_MEMBER,
#     "k_1": DurationFactorStrength.FIVE_DAYS,
#     "r": 0,
#     "L": 2700,
#     "L_ay": 450,
#     "restraint": BendingRestraint.DISCRETE_LATERAL_RESTRAINT_COMPRESSION_EDGE,
# }
# member = BoardMember(**member_dict)

# print(
#     "\n EG5.1 Design capacity timber formwork bearer \n"
#     f"Slenderness coefficient S1 = {member.S1} (ANS: 8.87) \n"
#     f"Stability factor k12 = {member.k_12_bend} (ANS: 1.0) \n"
#     f"Design moment capacity M_d = {member.M_d} (ANS: 9.75 kNm) \n"
#     f"(Note: k12 = 1 when compression edge lateral restraint < L_CLR, {member.L_ay} < {member.L_CLR})"
# )


# # Example 5.6 Design of a floor beam for the strength limit state
# from timberas.member import GlulamMember

# sec = TS.from_library("GL395x85")
# mat = TM.from_library("GL12")
# # mat.update_from_section_size(sec.d)
# member_dict = {
#     "sec": sec,
#     "mat": mat,
#     "application_cat": ApplicationCategory.PRIMARY_MEMBER,
#     "k_1": DurationFactorStrength.FIVE_DAYS,
#     "r": 0.25,
#     "L": 4000,
#     "L_ay": 450,
#     "restraint": BendingRestraint.DISCRETE_LATERAL_RESTRAINT_COMPRESSION_EDGE,
# }
# member = BoardMember(**member_dict)

# print(
#     "\n EG5.6 Design of a floor beam for the strength limit state \n"
#     "a) Bending capacity check, critical load case"
#     f"Slenderness coefficient S1 = {member.S1} (ANS: 6.39) \n"
#     f"Stability factor k12 = {member.k_12_bend} (ANS: 1.0) \n"
#     f"Design moment capacity M_d = {member.M_d} (ANS: 41.7 kNm) \n"
#     f"(Note: k12 = 1 when compression edge lateral restraint < L_CLR, {member.L_ay} < {member.L_CLR})"
# )
# print(
#     "b) Shear capacity check\n"
#     f"Design shear capacity V_d = {member.V_d} (ANS: 71.6 kNm) \n"
# )
# # SERVICEABILITY CHECK: TODO
# # BEARING CAPACITY CHECK: TODO
# member.update_k_1(DurationFactorStrength.FIFTY_YEARS)
# print(
#     "c) Bending capacity check, long-term load case \n"
#     f"Design moment capacity M_d = {member.M_d} (ANS: 25.3 kNm) \n"
#     f"Design shear capacity V_d = {member.V_d} (ANS: 43.5 kNm) \n"
# )
