####definitions and declarations related to rotations in a molecule
## ramificacion(matrixd, siunidosa, nounidosa)
## gtset(matrixg)
## dihedralrot(moleculae, imol, sua, nua, vectore, qdeg)
## rattle(moleculaf, qamplitud)
## build_initial_population(initial_structure,initial)
import numpy as np

####return the index of the molecules joined to "siunidosa", but
####in principle not joined to "nounidosa". If "siunidosa" and 
####"nounidosa" are in a ciclyc path, the return is a vector with
####all the elements as "1".
def ramificacion(matrixd, siunidosa, nounidosa):
    matrixdp = np.array(matrixd)
    matrixdp[siunidosa][nounidosa] = 0
    matrixdp[nounidosa][siunidosa] = 0
    nd=len(matrixdp)
    vectord=np.zeros(shape=(nd),dtype=np.int)
    vectordp=np.array(vectord)
    vectord[siunidosa] = 1
    sumd=1
    while sumd != 0:
        vectord = np.dot(matrixdp,vectord)
        vectord = [a + b for a, b in zip(vectord, vectordp)]
        vectord = map(lambda x: 0 if (x == 0) else 1,vectord)
        sumd = sum([a - b for a, b in zip(vectord, vectordp)])
        vectordp = vectord
    return vectord

####return the list of the bridges in a molecule.
def gtset(matrixg):
    gn = len(matrixg)
    bridgesetg = []
    for gi in range(0,gn):
        for gj in range(gi+1,gn):
            u = 1 if matrixg[gi][gj] != 0 else 0
            v = 1 if sum(matrixg[gi]) > 1 else 0
            w = 1 if sum(matrixg[gj]) > 1 else 0
            if ( u + v + w == 3 ):
                siuginougj = ramificacion(matrixg, gi, gj)
                alfa = sum(siuginougj)
                if ( alfa < gn ):
                    bridgeg = np.array([gi, gj])
                    bridgesetg.append(bridgeg)
    return bridgesetg

####return the same "moleculae" list with the molecule index "imol"
####rotate by an angle "qdeg" around the vector given by the "sua" and
####"nua" index. "vectore" is the list of the atoms that rotate.
def dihedralrot(moleculae, imol, sua, nua, vectore, qdeg):
    n_atoms=moleculae[imol,0,6]
    qrad = qdeg*np.pi/180.0
    eu0=(float(moleculae[imol,sua,1]) - float(moleculae[imol,nua,1]))
    ev0=(float(moleculae[imol,sua,2]) - float(moleculae[imol,nua,2]))
    ew0=(float(moleculae[imol,sua,3]) - float(moleculae[imol,nua,3]))
    mgt = np.sqrt(eu0*eu0+ev0*ev0+ew0*ew0)
    axisunitarivector = np.array([eu0, ev0, ew0])/mgt
    ex0=(float(moleculae[imol,sua,1]) + float(moleculae[imol,nua,1]))/2.0
    ey0=(float(moleculae[imol,sua,2]) + float(moleculae[imol,nua,2]))/2.0
    ez0=(float(moleculae[imol,sua,3]) + float(moleculae[imol,nua,3]))/2.0
    for iatoms in range(0,n_atoms):
        if ( vectore[iatoms] == 1 ):
            exi = float(moleculae[imol,iatoms,1]) - ex0
            eyi = float(moleculae[imol,iatoms,2]) - ey0
            ezi = float(moleculae[imol,iatoms,3]) - ez0
            evi = np.array([exi, eyi, ezi])
            tm1 = evi*(np.cos(qrad))
            tm2 = np.cross(axisunitarivector,evi)*np.sin(qrad)
            tm3 = axisunitarivector*(np.dot(axisunitarivector,evi))*(1.0 - np.cos(qrad))
            vri = tm1 + tm2 + tm3
            moleculae[imol,iatoms,1] = vri[0] + ex0
            moleculae[imol,iatoms,2] = vri[1] + ey0
            moleculae[imol,iatoms,3] = vri[2] + ez0

import random
from modulo_archivos import how_many_molecules
from modulo_utils import *
##TOMA UNA LISTA DE MOLECULAS (moleculaf) Y LE APLICA A CADA UNA
##PERTURBACIONES TORCIONALES EN UN ANGULO ALEATORIO (-qamplitud<=q<=qamplitud)
def rattle(moleculaf, qamplitud):
    total_molecules=how_many_molecules(moleculaf)
    moleculafp = moleculaf.copy() 
    for imol in range(1,total_molecules+1):
        n_atoms=moleculaf[imol,0,6]
        conmat=conectmx(moleculaf,imol)
        solution=gtset(conmat)
        nbridges=len(solution)
        #============================================
        #SE PUEDEN APLICAR DIFERENTES ENFOQUES RANDOM
        #============================================
        for ibridge in range(0,nbridges):
            sua=solution[ibridge][0]
            nua=solution[ibridge][1]
            list=ramificacion(conmat,sua,nua)
            qangle=random.randint(-qamplitud, qamplitud)
            dihedralrot(moleculafp, imol, sua, nua, list, qangle)
    return moleculafp

from modulo_archivos import jointab
##TOMA UNA MOLECULA DE ENTRADA (initial_structure) Y LE APLICA PERTURBACIONES
##TORCIONALES ALEATORIAS, GENERANDO UN NUMERO DE "initial" ESTRUCTURAS
def build_initial_population(initial_structure,initial):
    final=initial_structure.copy()
    for j in range(initial-1):
        moleculaf=initial_structure.copy()
        final=jointab(final,moleculaf)
    finalfm=rattle(final, 180)
    return finalfm
