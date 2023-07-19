
# Tension and Compression Capacity

Python code for the following examples are available in the Github repository [[example folder]](https://github.com/Folded-Structures-Lab/timber-as/tree/main/examples/tutorial_3.py). Several examples on this page are sourced from the *Timber Design Handbook* ([Standards Australia HB 108 - 2013](https://infostore.saiglobal.com/en-us/standards/sa-hb-108-2013-119982_saig_as_as_251451/)), written by Geoffrey Boughton and Keith Crews.


## Capacity Factor

Capacity factor phi is used to calculate the design capacities of structural timber; the value of phi varies based on material type and intended member application (*application category*, ref. Table 2.1 AS1720.1).

In *timberas*, capacity factors for all application categories as object attributes in the *TimberMaterial* class (*phi_1*, *phi_2*, *phi_3*). The *TimberMaterial.phi()* method is then used to select the approriate capacity factor based on an input application category. 

>*Example 2.11, Timber Design Handbook (page 163)*
> 
> Select the appropriate value for capacity factor phi for the following types of timber members:  
> (a) wall framing members in non-load bearing partitions, fabricated from MGP10; and  
> (b) members in a girder truss supporting ten roof trusses, fabricated from F17 seasoned Australian hardwood.


Solution: 
```
from timberas.material import TimberMaterial
from timberas.member import BoardMember, ApplicationCategory

#specify application category as integer 1, 2, or 3
material_a = TimberMaterial.from_library("MGP10")
application_category = 1
phi = material_a.phi(application_category)
print(f"Example 2.11(a) Solution MGP10 Frames phi = {phi} (ANS: 0.9)")

#or, specify application category from ApplicationCategory constants
material_b = TimberMaterial.from_library("F17 Seasoned Hardwood")
application_category = ApplicationCategory.GREATER_THAN_25_SQM
phi = material_b.phi(application_category)
print(f"Example 2.11(b) Solution Hardwood Trusses phi = {phi} (ANS=0.85)")
print(f"Application Category value = {application_category.value}")
```

Application category can be input as an integer value, or by using the *ApplicationCategory* enum class, which includes member applications listed in AS1720.1 Table 2.1 and their corresponding application category number.

## Tension Capacity


**TODO**

>*Example 3.3, Timber Design Handbook (page 188)*
> 
> A 190 x 35 MGP10 member is to be used as an internal principal member in a Brisbane stadium. The member end connections introduce 2 x 22mm diameter holes through the cross-section of the member. Evaluate the design tensile capacity for:  
> (a) a 50+ years duration load only; and  
> (b) a wind load combination

Solution: 
```
from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import BoardMember, DurationFactorStrength

#create a section and remove bolt holes from section tensile area
sec = TS.from_library("190x35")
sec.A_t = sec.A_g - 2 * 22 * sec.b  

#create a material and update properties from the section size
mat = TM.from_library("MGP10")
mat.update_from_section_size(sec.d)

#create a member
member = BoardMember(
    sec=sec, 
    mat=mat, 
    application_cat=2, 
    k_1=0.57,
    high_temp_latitude=False
)

print(
    "EG3.3(a) Design tensile capacity for permanent action case "
    f"(k_1 = {member.k_1}), N_dt = {member.N_dt} (ANS: 14.5 kN)"
)

#update the member load duration factor
member.update_k_1(DurationFactorStrength.FIVE_SECONDS)
print(
    "EG3.3(b) Design tensile capacity for wind action case "
    f"(k_1 = {member.k_1}), N_dt = {member.N_dt} (ANS: 25.4 kN)"
)
print(f"k_1={DurationFactorStrength.FIVE_SECONDS}={member.k_1}")

```


## Compression Capacity


**TODO**