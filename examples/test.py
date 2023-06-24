from timberas.material import MATERIAL_LIBRARY, TimberMaterial

print(MATERIAL_LIBRARY)

MGP10 = TimberMaterial.from_library('MGP10',MATERIAL_LIBRARY)

print(MGP10)


from timberas.geometry import TimberSection

stud_dict = {'name': '2/90x45', 'sec_type': 'rectangle', 'n': 2, 'b_i': 45, 'd': 90}
stud = TimberSection(**stud_dict)
print(stud)