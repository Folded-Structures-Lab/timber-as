

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
> TODO
> (a) 
Solution: 
```
from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import (
    BoardMember,
    ApplicationCategory,
    DurationFactorStrength,
    BendingRestraint,
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
    "restraint": BendingRestraint.DISCRETE_LATERAL_RESTRAINT_COMPRESSION_EDGE,
}
member = BoardMember(**member_dict)
member.report(["S1", "k_12_bend", "M_d", "L_CLR"])
#(ANS: S1 = 8.87, k_12_bend = 1.0, M_d = 9.75kNm)
```



Bending design parameters are derived from member inputs as follows:

- $\phi$, $k_1$, $k_4$, $k_6$ as described for previous capacities.
- Section modulus $Z$ is a *TimberSection* derived attribute. 
- Characteristic bending strength $f_b$ is a *TimberMaterial* attribute.
- Strength sharing factor $k_9$ (Ref. Cl 2.4.5) is implemented in *TimberMember* child classes:
    - For *GlulamMember*, $k_9$ always equals 1.0. 
    - For *BoardMember*, $k_9$ is evaluated from additional input *n_mem* (number of members spaced parellel to each other) and *s* (member spacing). Parameter *n_com* (number of elements fastened together in member) is a *TimberSection* attribute.
 
-  Stability factors for x-axis *k_12_x* and y-axis *k_12_y* buckling are derived from:
    - Material constant $\rho_C$ - requires a load-dependent ratio parameter $r$ (temporary design action / permanent design action).
    - Slenderness coefficients for x-axis *S_3* and y-axis *S_4* - requires member length *L* and effective length factor *g_13*. 
    - Intermediate lateral restraint will be discussed in the next section.



## Shear Capacity

The design shear capacity of timber member as per AS1720.1 Clause 3.2.5 is:
$$
M_{d} = \phi k_1 k_4 k_6 f_s A_s
$$
Input and evaluation of shear design parameters using *timberas* is detailed further with reference to the following example.


*Example 5.6, Timber Design Handbook (page 401)*:
> 
> TODO
> (a) 
Solution: 
```
from timberas.geometry import TimberSection as TS
from timberas.material import TimberMaterial as TM
from timberas.member import (
    GlulamMember,
    ApplicationCategory,
    DurationFactorStrength,
    BendingRestraint,
)

#(a) Permanent and short-term (5 day) load case
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
    "restraint": BendingRestraint.DISCRETE_LATERAL_RESTRAINT_COMPRESSION_EDGE,
}
member = GlulamMember(**member_dict)
member.report(["S1", "k_12_bend", "M_d", "V_d"])
#(ANS: S1 = 6.39, k_12_bend = 1.0, M_d = 41.7 kNm, V_d = 71.6 kN)

#(b) Permanent load case
member.update_k_1(DurationFactorStrength.FIFTY_YEARS)
member.report(["M_d", "V_d"])
#(ANS: M_d = 25.3 kNm, V_d = 43.5 kN)
```

Shear design parameters are derived from member inputs as follows:

- $\phi$, $k_1$, $k_4$, $k_6$ as described for previous capacities.
- Shear plane area $A_s$ is a *TimberSection* attribute, calculated as a reduction from gross area depending upon section shape type (e.g. *single_board* shapes have $A_s=2/3 A_g$)
- Characteristic shear strength $f_s$ is a *TimberMaterial* attribute.

