
# TODO

### Timber Handbook Capacity Examples
- [X] 3.1 f_t
- [X] 3.3 design tensile capacity Nd,t
- [X] 4.1 design compression capacity N_c
- [ ] 4.2 capacity of spaced columns
- [X] 4.3 load-bearing stud wall capacity check
- [X] 4.4 load-bearing stud wall capacity change
- [X] 5.1 bending design capacity
- [X] 5.6 floor beam design capacity


### Timber Handbook Design Examples
- [ ] 3.4 tension member design, seasoned timber
- [ ] 3.5 tension member design, unseasoned timber

### material.py
- update_from_section_size
    - implement interpolation between defined sizes for large sections
    - add A17

### section.py
- nominal vs actual section sizes

### member.py
- L_a different inputs for x-axis and y-axis compressive buckling?

### AS1684 loadings
- clean up code, change from functions to classes

# NOTES
- b is width of single stud member in block assembly, b_tot is total width.
- for S4 factor, b is assumed as width of single stud member (not total width).