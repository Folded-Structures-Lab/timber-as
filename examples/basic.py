from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import BoardMember, EffectiveLengthFactor

#define a section
sec = TS.from_library("2/90x45")

#define a material
mat = TM.from_library("MGP12")
member_dict = {
    "sec": sec,
    "mat": mat,
    "application_cat": 1,
    "g_13": EffectiveLengthFactor.PINNED_PINNED,
    "L": 2400,
    "L_ay": 600,
}
member = BoardMember(**member_dict)


print(f"Default design factors: k_1 = {member.k_1}, r={member.r}, k_6={member.g_13}")
print(f"EG4.1(a) Design compression capacity N_dc = {member.N_dc} (ANS: 3.54 kN)")
