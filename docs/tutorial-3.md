
# Tension and Compression Capacity

Python code for the following examples are available in the Github repository [[example folder]](https://github.com/Folded-Structures-Lab/timber-as/tree/main/examples/tutorial_3.py). Several examples on this page are sourced from the *Timber Design Handbook* ([Standards Australia HB 108 - 2013](https://infostore.saiglobal.com/en-us/standards/sa-hb-108-2013-119982_saig_as_as_251451/)), written by Geoffrey Boughton and Keith Crews.


## Capacity Factor

Capacity factor phi \phi is used to calculate the design capacities of structural timber; the value of phi varies based on material type and intended member application (*application category*, ref. Table 2.1 AS1720.1).

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
 the *member.update_k_1()* method to change the load duration factor and resolve member capacities 

>*Example 3.3, Timber Design Handbook (page 188)*
> 
> A 190 x 35 MGP10 member is to be used as an internal principal member in a Brisbane stadium. The member end connections introduce 2 x 22mm diameter holes through the cross-section of the member. Evaluate the design tensile capacity for:  
> (a) a 50+ years duration load only; and  
> (b) a wind load combination

Solution 3.3(a): 
```
from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import BoardMember, DurationFactorStrength

# create a section and remove bolt holes from section tensile area
sec = TS.from_library("190x35")
sec.A_t = sec.A_g - 2 * 22 * sec.b

# create a material and update properties from the section size
mat = TM.from_library("MGP10")
mat.update_from_section_size(sec.d)

# create a member
member = BoardMember(
    sec=sec, mat=mat, application_cat=2, k_1=0.57, high_temp_latitude=False
)

# output
member.report(["k_1", "N_dt"])
#(ANS: N_dt = 14.5 kN)"
```
The *member.report()* method is used to print a formatted report of the requested attribute names.

Solution 3.3(b), adding the following code:
```
# update member load duration factor and output
member.update_k_1(DurationFactorStrength.FIVE_SECONDS)
member.report(["k_1", "N_dt"], with_nomenclature=True, with_clause=True)
print("(ANS: N_dt = 25.4 kN)")

```
The *member.report()* function has parameters to enable additional detail in the printed report (attribute nomenclature and relevant clause(s) in AS1720.1). 

## Compression Capacity


**TODO**
The *member.solve_capacities()* method recalculates member capacites using the updated design parameter (g_13). 


>*Example 4.1, Timber Design Handbook (page 235)*
> 
> A 2.8m long, 190 x 35 MGP10 member is to be used as an internal principal member in a Brisbane stadium. Member end connections are bolted as per Example 3.3 and there is no intermediate lateral restraint in either direction.   

> (a) Evaluate the design compression capacity for a wind load combination.  
> (b) Compare the slenderness reduction factor S3 for pinned or semi-rigid end conditions.

Solution 4.1(a): 
```
from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import BoardMember, EffectiveLengthFactor

#create a section and remove bolt holes from section tensile area
sec = TS.from_library("190x35")

#create a material and update properties from the section size
mat = TM.from_library("MGP10")
mat.update_from_section_size(sec.d)


# assume pinned-pinned end fixity
g_13 = EffectiveLengthFactor.PINNED_PINNED
member.report("g_13")

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
member.report(["S3", "S4", "k_12_c", "N_dcx", "N_dcy", "N_dc"])
# (Ans: S3 = 14.7, S4 = 80, k_12_c = 0.042, N_dc = 3.54 kN)
```


Solution 4.1(b), adding the following code:

```
# update end fixity - assume as semi-rigid from bolt group
print("\nEG4.1(b) Compression Capacity - bolted ends")
member.g_13 = EffectiveLengthFactor.BOLTED_END_RESTRAINT
# resolve member capacities
member.solve_capacities()
# output
member.report(["g_13", "S3", "N_dcx"])
#(Ans: S3 = 11.1)
```


## Lateral Restraint