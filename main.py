#!/usr/bin/python 
import sys
import os
from os import sys,path,getcwd 
#====================================================================
#====================================================================
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
## Build initial population by kick methodology 
initial=10
njobs=8
ppj=4
file_initial="stage_1.molden"
### 
from modulo_archivos import readxyz, writexyz
initial_structure=readxyz('hexanoxxx.xyz')

from modulo_rotational import *
initial_population=build_initial_population(initial_structure,initial)
writexyz(initial_population,"initial.xyz")

from modulo_gaussian import *
#make_gaussian_inputs('T2500.bil',initial_population,1,'original')
#optimize_by_dft(njobs,ppj,"qgpu",1.0,"02:00:00")

##Get the geom from outputs gaussian 
#getouts=get_geometry_gaussian(file_initial,1,'all') 

exit()
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#====================================================================
#====================================================================


## get probabilities 
proba=get_fitness(getouts)
print proba
## rattle 
mol_rattle=rattle(getouts,90)
## crossover 

writexyz(mol_rattle,'p.xyz')


print "I found the end ..." 

## envir dft 
## ordenamos 

exit()
