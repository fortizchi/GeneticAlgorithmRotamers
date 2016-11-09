####definitions and declarations related to basical molecular properties
## covradii[]
## conectmx(molecule, imol)
import numpy as np

covradii={}
covradii["H"]=0.32
covradii["He"]=0.93
covradii["Li"]=1.23
covradii["Be"]=0.90
covradii["B"]=0.82
covradii["C"]=0.77
covradii["N"]=0.75
covradii["O"]=0.73
covradii["F"]=0.72
covradii["Ne"]=0.71
covradii["Na"]=1.54
covradii["Mg"]=1.36
covradii["Al"]=1.18
covradii["Si"]=1.11
covradii["P"]=1.06
covradii["S"]=1.02
covradii["Cl"]=0.99
covradii["Ar"]=0.98
covradii["K"]=2.03
covradii["Ca"]=1.74
covradii["Sc"]=1.44
covradii["Ti"]=1.32
covradii["V"]=1.22
covradii["Cr"]=1.18
covradii["Mn"]=1.17
covradii["Fe"]=1.17
covradii["Co"]=1.16
covradii["Ni"]=1.15
covradii["Cu"]=1.17
covradii["Zn"]=1.25
covradii["Ga"]=1.26
covradii["Ge"]=1.22
covradii["As"]=1.20
covradii["Se"]=1.16
covradii["Br"]=1.14
covradii["Kr"]=1.12
covradii["Rb"]=2.16
covradii["Sr"]=1.91
covradii["Y"]=1.62
covradii["Zr"]=1.45
covradii["Nb"]=1.34
covradii["Mo"]=1.30
covradii["Tc"]=1.27
covradii["Ru"]=1.25
covradii["Rh"]=1.25
covradii["Pd"]=1.28
covradii["Ag"]=1.34
covradii["Cd"]=1.48
covradii["In"]=1.44
covradii["Sn"]=1.41
covradii["Sb"]=1.40
covradii["Te"]=1.36
covradii["I"]=1.33
covradii["Xe"]=1.31
covradii["Cs"]=2.35
covradii["Ba"]=1.98
covradii["La"]=1.69
covradii["Ce"]=1.65
covradii["Pr"]=1.65
covradii["Nd"]=1.64
covradii["Pm"]=1.63
covradii["Sm"]=1.62
covradii["Eu"]=1.85
covradii["Gd"]=1.61
covradii["Tb"]=1.59
covradii["Dy"]=1.59
covradii["Ho"]=1.58
covradii["Er"]=1.57
covradii["Tm"]=1.56
covradii["Yb"]=1.74
covradii["Lu"]=1.56
covradii["Hf"]=1.44
covradii["Ta"]=1.34
covradii["W"]=1.30
covradii["Re"]=1.28
covradii["Os"]=1.26
covradii["Ir"]=1.27
covradii["Pt"]=1.30
covradii["Au"]=1.34
covradii["Hg"]=1.49
covradii["Tl"]=1.48
covradii["Pb"]=1.47
covradii["Bi"]=1.46
covradii["Po"]=1.46
covradii["At"]=1.45
covradii["Rn"]=1.90

def conectmx(molecule, imol):
    n_atoms=molecule[imol,0,6]
    matrixc=np.zeros(shape=(n_atoms,n_atoms),dtype=np.int)
    for iatoms in range(0,n_atoms):
        ri=covradii[molecule[imol,iatoms,0]]
        xi=float(molecule[imol,iatoms,1])
        yi=float(molecule[imol,iatoms,2])
        zi=float(molecule[imol,iatoms,3])
        for jatoms in range(iatoms+1,n_atoms):
            rj=covradii[molecule[imol,jatoms,0]]
            xj=float(molecule[imol,jatoms,1])
            yj=float(molecule[imol,jatoms,2])
            zj=float(molecule[imol,jatoms,3])
            distance = np.sqrt((xj - xi)**2 + (yj - yi)**2 + (zj - zi)**2)
            sumrad = ri + rj
            if ( distance <= 1.2*sumrad ):
                matrixc[iatoms][jatoms] = 1
                matrixc[jatoms][iatoms] = 1
    return matrixc
