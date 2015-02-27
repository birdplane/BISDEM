
================
Package Metadata
================

- **classifier**:: 

    Intended Audience :: Science/Research
    Topic :: Scientific/Engineering

- **description-file:** README.txt

- **entry_points**:: 

    [openmdao.component]
    wingse.aero.example=wingse.aero:Example
    birdplane.birdplane.Birdplane=birdplane.birdplane:Birdplane
    [openmdao.container]
    birdplane.aero.circulation.Circulation=birdplane.aero.circulation:Circulation
    birdplane.birdplane.Birdplane=birdplane.birdplane:Birdplane

- **keywords:** openmdao

- **name:** birdplane

- **requires-dist:** openmdao.main

- **requires-python**:: 

    >=2.7
    <3.0

- **static_path:** [ '_static' ]

- **version:** 0.1

