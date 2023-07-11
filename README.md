# timber-as
A Python package with tools to support research and design of Australian timber structures. *timberas* can be used to detemine the section properties, material properties, and design capacities for structural members as per Australian Standard AS1720.1:2020 (Timber Structures Part 1: Design Methods). 

# Main features
- Material and Section libraries: import 
- Design Capacity calculations: 


# Documentation:
Detailed information on *timberas* is available in package documentation at: [https://timberas.readthedocs.io/](https://timberas.readthedocs.io/). This includes background, calculation and design examples, and an API reference guide,


# Installation:
```
pip install timberas
```

# Getting Started:
A simple example for evaluating the design capacities
```

```

# Questionm Contibutions, and Feedback



# Acknowledgements and Citation
This package has been from research projects supported by the [University of Queensland](https://civil.uq.edu.au/), [ARC Future Timber Hub](https://futuretimberhub.org/) (2016-2021), and [ARC Advance Timber Hub](https://www.advance-timber-hub.org/) (2022-).


If you use *timberas* for projects or scientific publications, please consider citing our journal paper:
> Jiang, J., Ottenhaus, L. M., & Gattas, J. M. (2023). A parametric design framework for timber framing span tables. *Australian Journal of Civil Engineering*, 1-16. [doi:10.1080/14488353.2023.2227432](https://doi.org/10.1080/14488353.2023.2227432).


# License 



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

[ ] 5.1 bending design capacity

- nominal vs actual section sizes

- timberas.material.TimberMaterial.update_from_section_size
    - implement interpolation between defined sizes
    - add A17

# notes
- b is width of single stud member in block assembly, b_tot is total width
- for S4 factor, b is assumed as width of single stud member (not total width) - from AS1684 Cl?
