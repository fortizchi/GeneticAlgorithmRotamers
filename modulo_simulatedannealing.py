####definitions and declarations related to the simulated annealing in a molecule
## get_distance(mold)
## min_distance(ppp,molecule)
## perturbation(molecule,pp)
## perturbation2(molecule,pp)
## perturbation3(molecule,pp)
## perturbation_log(og,pert)

def get_distance(mold):
    how_many_atoms={}
    for key in sorted(mold.iterkeys()):
        how_many_atoms[key[0]]=key[1] 
    total_molecules=len(how_many_atoms)
    for imol in range(1,total_molecules+1):
             n_atoms=mold[imol,0,6]                          
             rmin=100.0 
             for i in range(n_atoms):
                   for j in range(i+1,n_atoms): 
                           rr=sqrt(((float(mold[imol,i,1]))**2)+((float(mold[imol,i,2]))**2)+((float(mold[imol,i,3]))**2))
                           if rmin >= rr:
                                   rmin=rr
    return rmin

def min_distance(ppp,molecule):
                import math 
                n_atoms=ppp[1,0,6]
                d=[]
                for i in range(n_atoms):
                        m=i+1
                        for j in range(m,n_atoms):
                                x1=float(ppp[1,i,1])
                                y1=float(ppp[1,i,2])
                                z1=float(ppp[1,i,3])
                                x2=float(ppp[1,j,1])
                                y2=float(ppp[1,j,2])
                                z2=float(ppp[1,j,3])
                                dx=(x2-x1)**2
                                dy=(y2-y1)**2
                                dz=(z2-z1)**2
                                di=math.sqrt(dx+dy+dz)
                                d.append(di)
                mi=min(d)
                if mi < 0.30: 
                        ppp=molecule.copy()
                        r=0
                else:
                        r=100
                return r

def perturbation(molecule,pp):
    how_many_atoms={}
    for key in sorted(molecule.iterkeys()):
        how_many_atoms[key[0]]=key[1] 
    total_molecules=len(how_many_atoms)
    ppp=molecule.copy() 
    for imol in range(1,total_molecules+1):
                r=0
                n_atoms=ppp[1,0,6]
                while r < 10:
                        pppa=molecule.copy() 
                        ri= random.randint(0,(n_atoms-1))
                        a1= random.uniform(-pp,pp)
                        ppp[imol,ri,1]=float(pppa[imol,ri,1])+random.uniform(-pp,pp)
                        ppp[imol,ri,2]=float(pppa[imol,ri,2])+random.uniform(-pp,pp)
                        ppp[imol,ri,3]=float(pppa[imol,ri,3])+random.uniform(-pp,pp)
                        r=min_distance(ppp,molecule)
                return ppp


def perturbation2(molecule,pp):
    ## "Function: make a perturbation in the original structure."
    how_many_atoms={}
    for key in sorted(molecule.iterkeys()):
        how_many_atoms[key[0]]=key[1] 
    total_molecules=len(how_many_atoms)
    ppp=molecule.copy()
    FACTOR=0.8660
    for imol in range(1,total_molecules+1):
                salida=0
                icounter=0
                while salida < 1: 
                        aaa=molecule.copy()
                        n_atoms=aaa[1,0,6]      
                        ri= random.randint(0,(n_atoms-1)) 
                        print "random", ri 
                        aaa[imol,ri,1]=float(ppp[imol,ri,1])+random.uniform(-pp,pp)
                        aaa[imol,ri,2]=float(ppp[imol,ri,2])+random.uniform(-pp,pp)
                        aaa[imol,ri,3]=float(ppp[imol,ri,3])+random.uniform(-pp,pp)
                        rmin=get_distance(aaa)
                        if rmin >= FACTOR:
                                salida=2
                        icounter+=1 
                        if icounter >10000:
                                icounter=0
                                FACTOR=FACTOR-0.1
                        if FACTOR < 0.25:
                                FACTOR=0.25 
    return aaa

def perturbation3(molecule,pp):
    ## "Function: make a perturbation in the original structure."
    how_many_atoms={}
    for key in sorted(molecule.iterkeys()):
        how_many_atoms[key[0]]=key[1] 
    total_molecules=len(how_many_atoms)
    ppp=molecule.copy()
    FACTOR=0.8660
    #for imol in range(1,total_molecules+1):
    imol=1
    aaa={} 
    aaa=molecule.copy()
    n_atoms=aaa[1,0,6]  
    ri= random.randint(0,(n_atoms-1)) 
    #print "random", ri 
    aaa[imol,ri,1]=float(ppp[imol,ri,1])+random.uniform(-pp,pp)
    aaa[imol,ri,2]=float(ppp[imol,ri,2])+random.uniform(-pp,pp)
    aaa[imol,ri,3]=float(ppp[imol,ri,3])+random.uniform(-pp,pp)
                        
    return aaa

def perturbation_log(og,pert):
        mole=[]
        n_atoms=og[1,0,6]
        imol=1
        for i in range(n_atoms):
                for j in range(i+1,n_atoms):
                         rr1=sqrt(((float(og[imol,i,1]))**2)+((float(og[imol,i,2]))**2)+((float(og[imol,i,3]))**2))
                         rr2=sqrt(((float(pert[imol,i,1]))**2)+((float(pert[imol,i,2]))**2)+((float(pert[imol,i,3]))**2))
                         dr=rr2-rr1
                         print "Atoms",i,j
                         print "Distances", dr
