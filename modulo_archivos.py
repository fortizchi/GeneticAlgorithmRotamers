####definitions and declarations related to import and export .molden/.xyz files
## how_many_molecules(inmolk
## readxyz(filename)
## writexyz(molecule,output)
## choose_one_molecule(molecule,in_idx)
## jointab(aaa,bbb)

def how_many_molecules(inmolk):
    molka=inmolk.copy()
    how_many_atoms={}
    for key in sorted(molka.iterkeys()):
        how_many_atoms[key[0]]=key[1] 
    total_molk=len(how_many_atoms)
    molka.clear()
    return total_molk

def readxyz(filename):
	hd=open(filename,'r')
	coordx=[]
	coordy=[]
	coordz=[]
	atoms=[]
        geometry={}
        imol=0
	energy=0.0
	name="unknown"
	for line in hd:
		ls=line.split()
                if len(ls)==1:
                    n_atoms=ls[0]
                    iatoms=0
		    imol=imol+1
                if len(ls)==2:
                    energy=ls[0]
                    name=ls[1]
		if len(ls)==4:
                    geometry[imol,iatoms,0]=ls[0]
		    geometry[imol,iatoms,1]=ls[1]
		    geometry[imol,iatoms,2]=ls[2]
		    geometry[imol,iatoms,3]=ls[3]
		    geometry[imol,0,4]=energy
		    geometry[imol,0,5]=name
                    iatoms=iatoms+1
		    geometry[imol,0,6]=iatoms
	return geometry 

def writexyz(molecule,output):
    open_new = open(output,"w")
    total_molecules=how_many_molecules(molecule)
    for imol in range(1,total_molecules+1):
        n_atoms=molecule[imol,0,6]
        energy=float(molecule[imol,0,4])
        name=molecule[imol,0,5]
        print >>open_new,"%-4d" % (n_atoms)
        print >>open_new,"%-16.9f %s %s" % (energy,"  ",name)
        for iatoms in range(0,n_atoms):
            sym=molecule[imol,iatoms,0]
            xx=float(molecule[imol,iatoms,1])
            yy=float(molecule[imol,iatoms,2])
            zz=float(molecule[imol,iatoms,3])
            print >>open_new,"%-2s %16.9f %16.9f %16.9f" % (sym,xx,yy,zz)
    open_new.close()
    print "Output = ",output 

def choose_one_molecule(molecule,in_idx):
    total_molecules=how_many_molecules(molecule)
    if  in_idx == 0:
        in_idx=1
    if ( in_idx > (total_molecules)):
             print "Warning: There are not ",in_idx,"molecules, there are only",total_molecules
             in_idx=total_molecules
    salida={}
    for imol in range(1,total_molecules+1):
        n_atoms=molecule[imol,0,6]
        energy=float(molecule[imol,0,4])
        name=molecule[imol,0,5]                            
        if  imol == in_idx:
             salida[1,0,6]=n_atoms
             salida[1,0,4]=energy
             salida[1,0,5]=name
             for iatoms in range(0,n_atoms):
                  sym=molecule[imol,iatoms,0]
                  xx=float(molecule[imol,iatoms,1])
                  yy=float(molecule[imol,iatoms,2])
                  zz=float(molecule[imol,iatoms,3])
                  salida[1,iatoms,0]=sym
                  salida[1,iatoms,1]=xx
                  salida[1,iatoms,2]=yy
                  salida[1,iatoms,3]=zz
    return salida

def jointab(aaa,bbb):
    total_molecules1=(how_many_molecules(aaa))
    total_molecules2=(how_many_molecules(bbb))
    mtodas={}
    iim=1
    for imol in range(1,total_molecules1+1):
        name_m="name_"+str(iim).zfill(4)
        n_atoms=aaa[imol,0,6]
        energy=aaa[imol,0,4]
        mtodas[iim,0,6]=n_atoms
        mtodas[iim,0,5]=name_m
        mtodas[iim,0,4]=energy
        for iatoms in range(0,n_atoms):
            sym=aaa[imol,iatoms,0]
            xx=aaa[imol,iatoms,1]
            yy=aaa[imol,iatoms,2]
            zz=aaa[imol,iatoms,3]
            mtodas[iim,iatoms,0]=sym
            mtodas[iim,iatoms,1]=xx
            mtodas[iim,iatoms,2]=yy
            mtodas[iim,iatoms,3]=zz
        iim=iim+1
    for imol in range(1,total_molecules2+1):
        name_m="name_"+str(iim).zfill(4)
        n_atoms=bbb[imol,0,6]
        energy=bbb[imol,0,4]
        mtodas[iim,0,6]=n_atoms
        mtodas[iim,0,5]=name_m
        mtodas[iim,0,4]=energy
        for iatoms in range(0,n_atoms):
            sym=bbb[imol,iatoms,0]
            xx=bbb[imol,iatoms,1]
            yy=bbb[imol,iatoms,2]
            zz=bbb[imol,iatoms,3]
            mtodas[iim,iatoms,0]=sym
            mtodas[iim,iatoms,1]=xx
            mtodas[iim,iatoms,2]=yy
            mtodas[iim,iatoms,3]=zz
        iim=iim+1
    return mtodas
