# timber-as
 A Python package with tools to support the design of timber structures to Australian Standards


# todos
docstring AS1684
examples

[X] 3.1 f_t
n/a 3.2 k1 factor
[X] 3.3 design tensile capacity Nd,t
[ ] 3.4 tension member design, seasoned timber
[ ] 3.5 tension member design, unseasoned timber

[X] 4.1 design compression capacity N_c
[ ] 4.2 capacity of spaced columns
[X] 4.3 load-bearing stud wall capacity check
[X] 4.4 load-bearing stud wall capacity change

- timberas.material.TimberMaterial.update_from_section_size
    - implement interpolation between defined sizes
    - add A17

# notes
- b is width of single stud member in block assembly, b_tot is total width
- for S4 factor, b is assumed as width of single stud member (not total width) - from AS1684 Cl?



 python3.10 -m venv env
 activate env
 pip install -r requirements.txt
 pip install --editable . 

