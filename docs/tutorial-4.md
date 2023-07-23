

# Bending and Shear Capacity

Python code for the following examples are available in the Github repository [examples folder](https://github.com/Folded-Structures-Lab/timber-as/tree/main/examples/tutorial_4.py). Several examples on this page are sourced from the *Timber Design Handbook* ([Standards Australia HB 108 - 2013](https://infostore.saiglobal.com/en-us/standards/sa-hb-108-2013-119982_saig_as_as_251451/)), written by Geoffrey Boughton and Keith Crews.


## Bending Capacity


The design bending capacity of timber member as per AS1720.1 Clause 3.2.1 is:
$$
M_{d} = \phi k_1 k_4 k_6 k_9 k_{12} f_b Z
$$

<!-- The stability factor for lateral bucking under bending $k_{12}$ (Ref. Cl 3.2.3) accounts for the [].
Thus, *timberas* evaluates stability and bending capacity about both axes, using then then minimum as the governing design compressive capacity: -->

Input and evaluation of bending design parameters using *timberas* is detailed further with reference to the following example.

*Example 5.1, Timber Design Handbook (page 333)*:
> 
> Check the bending design capacity of a formwork bearer. The bearer spans 2.7m, is a nominal 250 mm x 50 mm section, and is made from unseasoned F11 messmate timber. Joists are skew-nailed to the top edge of the bearer at 450mm centres.
> 

Solution: 
```
from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import (
    BoardMember,
    ApplicationCategory,
    DurationFactorStrength,
    RestraintEdge,
)

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

#(ANS: k_12_bend = 1.0, M_d = 9.75kNm)
```



Bending design parameters are derived from member inputs as follows:

- $\phi$, $k_1$, $k_4$, $k_6$ as described for previous capacities.
- Section modulus $Z$ is a *TimberSection* derived attribute. 
- Characteristic bending strength $f_b$ is a *TimberMaterial* attribute.
- Strength sharing factor $k_9$ (Ref. Cl 2.4.5) is implemented in *TimberMember* child classes:
    - For *GlulamMember*, $k_9$ always equals 1.0. 
    - For *BoardMember*, $k_9$ is evaluated from additional input *n_mem* (number of members spaced parallel to each other) and *s* (member spacing). Parameter *n_com* (number of elements fastened together in member) is a *TimberSection* attribute.
-  Stability factor for bending $k_{12}$  (Ref. Cl 3.2.4) is derived from:
    - Material constant $\rho_B$ - requires a load-dependent ratio parameter $r$ (temporary design action / permanent design action).
    - Slenderness coefficient $S1$ - requires lateral restraint information (distance between restraint and restrained edge condition).

Distance between lateral restraints on the tension or compression edge is $L_{ay}$, using the same input as for lateral restraint against compressive buckling:
```
"L_a": {"x": None, "y": 450}
```

The restraint edge condition is specified with the *restraint_edge* attribute. This accepts a string value (e.g. "compression" for compression edge) or a *RestraintEdge* enum class attribute; the latter gives type-safe input of available restraint edge conditions.
```
"restraint_edge": RestraintEdge.COMPRESSION,
```
The timber member will self-evaluate whether the distance between lateral restraints is sufficient to provide continuous lateral restraint (CLR). If $L_{ay}<=L_{CLR}$, the member is considered continuously restrained (*CLR* = True). If not, it is considered as having discrete restraints (*CLR*=False).

For the special case of continuous tension edge restraint with discrete torsional restraint, distance between torsional restraints is provided with a *phi* key in the *L_a* input dictionary:
```
"restraint_edge": RestraintEdge.TENSION_AND_TORSIONAL,
"L_a": {"x": None, "y": 450, "phi" = 900}
``` 

Bending capacity is currently evaluated about the x-axis only, using $S1$ if the $x$ direction is the major axis ($k_{12}<=1.0$), or $S2$ otherwise if $x$ is the minor axis ($k_{12}=1.0$). 

## Shear Capacity

The design shear capacity of timber member as per AS1720.1 Clause 3.2.5 is:
$$
M_{d} = \phi k_1 k_4 k_6 f_s A_s
$$
Input and evaluation of shear design parameters using *timberas* is detailed further with reference to the following example.


*Example 5.6, Timber Design Handbook (page 401)*:
> 
> Evaluate the design bending and shear capacities of a GL12 floor beam member under a:
> (a) permanent and short-term (5 day) load case; and
> (b) permanent load case  
> The floor beam has a 4 m design span and supports an office floor in a building in Victoria. Joists are attached to the top of the beam with nailed straps at 450 mm spacing. 
Solution: 
```
from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import (
    GlulamMember,
    ApplicationCategory,
    DurationFactorStrength,
    RestraintEdge,
)

#(a) Permanent and short-term (5 day) load case"
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
#(ANS: k_12_bend = 1.0, M_d = 41.7 kNm, V_d = 71.6 kN)

#(b) Permanent load case
member.update_k_1(DurationFactorStrength.FIFTY_YEARS)
member.report(["M_d", "V_d"])
#(ANS: M_d = 25.3 kNm, V_d = 43.5 kN)
```

Shear design parameters are derived from member inputs as follows:

- $\phi$, $k_1$, $k_4$, $k_6$ as described for previous capacities.
- Shear plane area $A_s$ is a *TimberSection* attribute, calculated as a reduction from gross area depending upon section shape type (e.g. *single_board* shapes have $A_s=2/3 A_g$)
- Characteristic shear strength $f_s$ is a *TimberMaterial* attribute.

