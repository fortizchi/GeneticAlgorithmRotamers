####definitions and declarations related to soon generation by bridge split.
####the selection of the parents follow a probability distribution from a
####previous estimation of the total energy.
## edgealineator(moleculag, imol, gvi, gvj)
## weightedChoice(weights, objects)
## ruleta(moleculaxi, nofsons)
## soongenerator(moleculai,moleculaj)
## multisoongenerator(moleculaset,soonlist)

from modulo_archivos import how_many_molecules, choose_one_molecule, jointab
from modulo_utils import *
from modulo_rotational import *
import random
import numpy as np
from numpy import cumsum
from numpy.random import rand

def edgealineator(moleculag, imol, gvi, gvj):
    vz=np.array([0.0, 0.0, 1.0]) 
    vo=np.array([0.0, 0.0, 0.0]) 
    n_atoms=moleculag[imol,0,6]
    gu0 = (float(moleculag[imol,gvj,1]) - float(moleculag[imol,gvi,1]))
    gv0 = (float(moleculag[imol,gvj,2]) - float(moleculag[imol,gvi,2]))
    gw0 = (float(moleculag[imol,gvj,3]) - float(moleculag[imol,gvi,3]))
    mgt = np.sqrt(gu0*gu0+gv0*gv0+gw0*gw0)
    gv1 = np.array([gu0, gv0, gw0])/mgt
    ##DEFINICION DEL TMATRIX
    if ( np.cross(gv1,vz) == vo).all():
        tmatrix = np.identity(3)
    else:
        m1 = np.array([gv1[1], -gv1[0], 0.0])
        m2 = np.cross(gv1,m1)
        tmatrix = np.array([m1, m2, gv1])
    gx0 = (float(moleculag[imol,gvj,1]) + float(moleculag[imol,gvi,1]))/2.0
    gy0 = (float(moleculag[imol,gvj,2]) + float(moleculag[imol,gvi,2]))/2.0
    gz0 = (float(moleculag[imol,gvj,3]) + float(moleculag[imol,gvi,3]))/2.0
    for gi in range(0,n_atoms):
        gxi = float(moleculag[imol,gi,1]) - gx0
        gyi = float(moleculag[imol,gi,2]) - gy0
        gzi = float(moleculag[imol,gi,3]) - gz0
        gv2 = np.array([gxi, gyi, gzi])
        vri = np.dot(tmatrix, gv2)
        moleculag[imol,gi,1] = vri[0]
        moleculag[imol,gi,2] = vri[1]
        moleculag[imol,gi,3] = vri[2]

def weightedChoice(weights, objects):
    cs = cumsum(weights)
    idx = sum(cs < rand())
    return objects[idx]

def ruleta(moleculaxi, nofsons):
    total_molecules=how_many_molecules(moleculaxi)
    energyset = []
    for imol in range(1,total_molecules+1):
        n_atoms=moleculaxi[imol,0,6]
        energy =moleculaxi[imol,0,4]
        energyset.append(float(energy))
    #-------------------------
    m=len(energyset)
    delx=max(energyset)/m
    list1=[float(1.0/(x+delx)) for x in energyset]
    list2=np.array(list1)/sum(list1)
    objects=range(1,m+1)
    #-------------------------
    nset = []
    for imol in range(0,nofsons):
        ri=weightedChoice(list2, objects)
        rj=weightedChoice(list2, objects)
        nset.append([ri,rj])
    return nset

def soongenerator(moleculai,moleculaj):
    natomsi=moleculai[1,0,6]
    natomsj=moleculaj[1,0,6]
    hijoi = moleculai.copy()
    hijoj = moleculaj.copy()
    #-------------------------
    mx1=conectmx(moleculai,1)
    bridgeset1=gtset(mx1)
    list1L=[sum(ramificacion(mx1,x[0],x[1])) for x in bridgeset1]
    n=len(mx1)
    list1P=[abs(n - 2*x) for x in list1L]
    #-------------------------
    list1=list(set(list1P))
    m=len(list1)
    list2=[float(1.0/(x+1.0)) for x in list1]
    list3=np.array(list2)/sum(list2)
    objects=range(m)
    rp=weightedChoice(list3, objects)
    ef=list1[rp]
    #-------------------------
    index1=list1P.index(ef)
    bridge1=bridgeset1[index1]
    padre1=moleculai.copy()
    edgealineator(padre1, 1, bridge1[0], bridge1[1])
    #-------------------------
    mx2=conectmx(moleculaj,1)
    bridgeset2=gtset(mx2)
    list2L=[sum(ramificacion(mx2,x[0],x[1])) for x in bridgeset2]
    list2P=[abs(n - 2*x) for x in list2L]
    index2=list2P.index(ef)
    bridge2=bridgeset2[index2]
    padre2=moleculaj.copy()
    edgealineator(padre2, 1, bridge2[0], bridge2[1])
    #-------------------------
    rmf1=ramificacion(mx1,bridge1[0],bridge1[1])
    dn1=[i for i,x in enumerate(rmf1) if x == 1]
    up1=[i for i,x in enumerate(rmf1) if x == 0]
    rmf2=ramificacion(mx2,bridge2[0],bridge2[1])
    dn2=[i for i,x in enumerate(rmf2) if x == 1]
    up2=[i for i,x in enumerate(rmf2) if x == 0]
    for hi in range(0,natomsi):
        if(hi < len(up1)):
            hijoi[1,hi,0]=padre1[1,up1[hi],0]
            hijoi[1,hi,1]=padre1[1,up1[hi],1]
            hijoi[1,hi,2]=padre1[1,up1[hi],2]
            hijoi[1,hi,3]=padre1[1,up1[hi],3]
        else: 
            hijoi[1,hi,0]=padre2[1,dn2[hi-len(up1)],0]
            hijoi[1,hi,1]=padre2[1,dn2[hi-len(up1)],1]
            hijoi[1,hi,2]=padre2[1,dn2[hi-len(up1)],2]
            hijoi[1,hi,3]=padre2[1,dn2[hi-len(up1)],3]
        if(hi < len(up2)):
            hijoj[1,hi,0]=padre2[1,up2[hi],0]
            hijoj[1,hi,1]=padre2[1,up2[hi],1]
            hijoj[1,hi,2]=padre2[1,up2[hi],2]
            hijoj[1,hi,3]=padre2[1,up2[hi],3]
        else: 
            hijoj[1,hi,0]=padre1[1,dn1[hi-len(up2)],0]
            hijoj[1,hi,1]=padre1[1,dn1[hi-len(up2)],1]
            hijoj[1,hi,2]=padre1[1,dn1[hi-len(up2)],2]
            hijoj[1,hi,3]=padre1[1,dn1[hi-len(up2)],3]
    hindex=random.randint(0, 1)
    if(hindex == 0):
        hijo = hijoi.copy()
    else:
        hijo = hijoj.copy()
    return hijo

def multisoongenerator(moleculaset,soonlist):
    nofsoons=len(soonlist)
    for sk in range(0,nofsoons):
        si=soonlist[sk][0]
        sj=soonlist[sk][1]
        moleculai=choose_one_molecule(moleculaset,si)
        moleculaj=choose_one_molecule(moleculaset,sj)
        mhijo=soongenerator(moleculai,moleculaj)
        if(sk == 0):
            hijo0=mhijo
        else:
            hijo0=jointab(hijo0,mhijo)
    return hijo0
