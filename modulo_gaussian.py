####definitions and declarations related to use of the gaussian code
## is_number(s)
## read_block2(filename)
## write_input_gaussian(molecule,output)
## send_dft(gg0,fileg)
## read_geometry(fileg)
## get_energy(g)
## read_block1_of_bil(filename)
## make_gaussian_inputs(bilatu_file,MOLmolden,number_block,name_original)
## get_geometry_gaussian(output,zpe,normal_input)
from queue_system2 import *

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

def read_block2(filename):
    data_block2=[]
    bilfile=open(filename,"r")
    printer=0
    for line in bilfile:
             lin = line.lstrip()
             if lin.startswith("---block1---"):
                 printer=1+printer
             if printer == 1 and not lin.startswith("---block1---"):
                 data_block2.append(line)                
    return data_block2

def write_input_gaussian(molecule,output):
    data=read_block2('annie.an')
    how_many_atoms={}
    for key in sorted(molecule.iterkeys()):
        how_many_atoms[key[0]]=key[1] 
    total_molecules=len(how_many_atoms) 
    for imol in range(1,total_molecules+1):
        open_new = open(output,"w")
        n_atoms=molecule[imol,0,6]
        energy=float(molecule[imol,0,4])
        name=molecule[imol,0,5]
        for ii in range(0,len(data)):
                open_new.write(data[ii])        
        for iatoms in range(0,n_atoms):
            sym=molecule[imol,iatoms,0]
            xx=float(molecule[imol,iatoms,1])
            yy=float(molecule[imol,iatoms,2])
            zz=float(molecule[imol,iatoms,3])
            print >>open_new,"%-2s %16.9f %16.9f %16.9f" % (sym,xx,yy,zz)
        print >>open_new," "
        open_new.close()
        #print "Making Gaussian Input = ",output 

def send_dft(gg0,fileg):
        write_input_gaussian(gg0,nameinp)
        fileo=fileg.split(".")[0]+str(".out")
        dft="g09 < "+ str(fileg)+ " > "+str(fileo)
        cmd="rm -rf Gau-*"
        os.system(dft)
        os.system(cmd)

def read_geometry(fileg):
        geometry={}
        g09file=open(fileg,'r')
        atoms, coord, vibfreq, vibmode = [], [], [], []
        n_atoms=0
        ENERGY=0.0
        CORRECTO=0
        suc=0
        for line in g09file:
                 ls=line.split()
                 if "SCF Done" in line:
                        ENERGY=float(line.split()[4])
                        CORRECTO=1
                 if line.strip() in ("Input orientation:", "Standard orientation:"):  
                        for ii in range(4): g09file.next()
                        line=g09file.next()
                        n_atoms=0
                        atoms=[]
                        coordx=[]
                        coordy=[]
                        coordz=[]
                        while not line.startswith(" --------"):
                            ls = line.split()
                            if (len(ls) == 6 and ls[0].isdigit() and ls[1].isdigit() and ls[2].isdigit()):
                                atoms.append(int(ls[1]))
                                coordx.append(float(ls[3]))
                                coordy.append(float(ls[4]))
                                coordz.append(float(ls[5]))
                                n_atoms=n_atoms+1
                            else:
                                break
                            line=g09file.next()
        imol=1
        if n_atoms > 0:
                geometry[imol,0,4] = ENERGY
                geometry[imol,0,5] = fileg
                geometry[imol,0,6] = n_atoms
                for iatoms in range(len(coordx)):
                        geometry[imol,iatoms,0] = elementos[atoms[iatoms]] 
                        geometry[imol,iatoms,1] = coordx[iatoms]
                        geometry[imol,iatoms,2] = coordy[iatoms]
                        geometry[imol,iatoms,3] = coordz[iatoms]
                suc=1 
        else: 
                suc=0
        return geometry, suc

def get_energy(g):
        ggg={}
        ggg=g.copy()
        energy1=ggg[1,0,4]
        return energy1

def read_block1_of_bil(filename):
    bilfile=open(filename,"r")
    ppnode=16 #default value 
    defqueue="qgpu"
    for line in bilfile:
        line=line.strip(' \t\n\r')
        if len(line.strip()) != 0 :
           li = line.lstrip()
           if not li.startswith("#"):
              readline=line.split()
              if len(readline) == 2:
                 data0=readline[0].strip('\t\n\r') 
                 data1=readline[1].strip('\t\n\r')
                 if data0.lower() == "nprocshared":
                    ppnode=data1
                 if data0.lower() == "queue":
                    defqueue=data1
                    #cabellitos
    if defqueue == "qgpu":
       ppnode=10
    if defqueue == "qintel":
       ppnode=16
    nodestotal="%NProcShared="+str(ppnode)+"\n"
    bilfile.close() 
    data_block1=[]
    #data_block1.append(nodestotal) 
    if not os.path.isfile(filename):
        print "File not exist ::",filename 
        sys.exit()
    else:    
        bilfile=open(filename,"r")
        printer=0
        for line in bilfile:
             lin = line.lstrip()
             if lin.startswith("---block1---"):
                 printer=1+printer
             if printer == 1 and not lin.startswith("---block1---"):
                 data_block1.append(line)                
    return data_block1

def make_gaussian_inputs(bilatu_file,MOLmolden,number_block,name_original):
    molecule=MOLmolden.copy()
    data_block1=read_block1_of_bil(bilatu_file)
    data_block2=read_block1_of_bil(bilatu_file)
    how_many_atoms={}
    for key in sorted(molecule.iterkeys()):
        how_many_atoms[key[0]]=key[1] 
    total_molecules=len(how_many_atoms) 
    for imol in range(1,total_molecules+1):
        n_atoms=molecule[imol,0,6]
        energy=molecule[imol,0,4]
        name=molecule[imol,0,5]
        num=str(imol).zfill(4)
        if name_original == "original":
            namm=name.split(".")
            nameout=namm[0]+".inp"
        else: 
            nameout="moo_"+num+".inp"
        fh=open(nameout,"w")
        print "Making input =",nameout
        if int(number_block) == int(1):
            for ii in range(0,len(data_block1)):
                fh.write(data_block1[ii])
        if int(number_block) == int(2):
            for ii in range(0,len(data_block2)):
                fh.write(data_block2[ii])
        for iatoms in range(0,n_atoms):
             sym=molecule[imol,iatoms,0]
             xx=float(molecule[imol,iatoms,1])
             yy=float(molecule[imol,iatoms,2])
             zz=float(molecule[imol,iatoms,3])
             print >>fh,"%-2s %16.9f %16.9f %16.9f" % (sym,xx,yy,zz)
        fh.write("  \n") 
        fh.close()

def get_geometry_gaussian(output,zpe,normal_input):
    ## get_geometry_gaussian(output,1,'all')
    ## get_geometry_gaussian(output,1,'1')
    i=0
    hartree2kcalmol=float(627.51)
    all_energy_scf=[]
    all_energy_zpe=[]
    all_charge=[]
    all_multi=[]
    all_freq=[]
    all_freq_min=[]
    all_files=[]
    all_normal=[]
    all_bases=[]
    all_functional=[]
    all_ccsdt=[]
    all_opti=[]
    all_iscf=[]
    print "Getting data ..."
    for file in glob.glob("*.out"):
        if path.isfile(file):
            i=i+1
            g09file=open(file,'r')
            energy_scf=float(0.0)
            energy_zpe=float(0.0)
            energy_ccsdt=float(0.0)
            ccsdt=float(0.0)
            charge=0
            multip=1
            freq_negative=0
            freq_by_file=[]
            freq_true=False
            normal=0
            freq_min=float(0.0)
            functional="unknown"
            funcional="unknown"
            base="unknown"
            optimization="No_Opti"
            optimization="No_Opti"
            #print file
            funk="" 
            iscf=0
            for line in g09file:
                #print line 
                if line.strip():
                    lin=line.split()
                    funk=line.lstrip()
                    #print "perro ",funk
                if re.search('^# BP86',funk):
                    func=funk.split() 
                    funcional=func[1]
                    base=func[2]    
                if re.search('^# PW91PW91',funk):
                    func=funk.split() 
                    funcional=func[1]
                    base=func[2]
                if re.search('^# PBE1PBE',funk):
                    func=funk.split() 
                    funcional=func[1]
                    base=func[2]
                if re.search('^# M06',funk):
                    func=funk.split() 
                    funcional=func[1]
                    base=func[2]
                if re.search('^# B3LYP',funk):
                    func=funk.split() 
                    funcional=func[1]
                    base=func[2]
                if re.search('^# BLYP',funk):
                    func=funk.split() 
                    funcional=func[1]
                    base=func[2]
                if re.search('^# GEN',funk):
                    func=funk.split() 
                    funcional=func[1]
                    base=func[2]
                
                #if re.search('^# M062X',funk):
                #    func=funk.split() 
                #    funcional=func[1]
                #    base=func[2]
                #if re.search('^# M052X',funk):
                #    func=funk.split() 
                #    funcional=func[1]
                #    base=func[2]
                if "SCF Done" in line:
                    scf=line.split()
                    energy_scf=scf[4]
                    iscf=iscf+1
                if "Zero-point correction=" in line: 
                    zpc=line.split()
                    energy_zpe=zpc[2]
                if "Charge" and "Multiplicity" in line:
                    charge0=line.split()
                    charge=charge0[2]
                    multip=charge0[5]
                if "Frequencies" in line:
                    freq_true=True
                    freq=line.split()
                    for ifreq in range(2,5):
                        if freq[ifreq] < 0.0:
                            freq_negative=freq_negative+1
                        else:
                            freq_by_file.append(freq[ifreq])
                if "Normal termination" in line: 
                    normal=normal+1
                #if "CCSD(T)=" in line:
                #    ccsdtl=line.split()
                #    #print ccsdtl 
                #    if ccsdtl[0] == "CCSD(T)=":
                #        ccsdt= ccsdtl[1]
                #if line[1:9] == "CCSD(T)=":
                #    energy_ccsdt_tmp=line.split()[1]
                #    ## Convert a string to a float avoiding the problem with Ds.
                #    energy_ccsdt_tmp= energy_ccsdt_tmp.replace("D","E")
                #    energy_ccsdt=float(energy_ccsdt_tmp)
                #    #print energy_ccsdt 
                #if  "Optimization completed." in line:
                #     optimization="Optimization" 
                #if  "Rotational constants (GHZ):" in line: 
                #     rcons=line.split()
                #     rc1=float(rcons[3])
                #     rc2=float(rcons[4])
                #     rc3=float(rcons[5])
                if freq_true:
                    freq_by_file.sort(key=float)
                    freq_min=freq_by_file[0]
        
            if zpe == 1:
                energy_s=float(energy_scf)+float(energy_zpe)
            else: 
                energy_s=float(energy_scf)
 
            all_energy_scf.append(float(energy_s))
            all_energy_zpe.append(float(energy_zpe))
            all_charge.append(charge)
            all_multi.append(multip)
            all_freq.append(freq_negative)
            all_freq_min.append(freq_min)
            all_files.append(file)
            all_normal.append(normal)
            all_bases.append(base)
            all_functional.append(funcional)
            all_ccsdt.append((ccsdt))
            all_opti.append(optimization)
            all_iscf.append(iscf)
    ## for now just i need the energy and the files           
    for i in range( len(all_energy_scf) ):
        for k in range( len(all_energy_scf) - 1, i, -1 ):
            if ( all_energy_scf[k] < all_energy_scf[k-1] ):
                tmp=all_energy_scf[k]
                all_energy_scf[k]=all_energy_scf[k-1]
                all_energy_scf[k-1]=tmp
                tmp=all_files[k]
                all_files[k]=all_files[k-1]
                all_files[k-1]=tmp
                tmp=all_ccsdt[k]
                all_ccsdt[k]=all_ccsdt[k-1]
                all_ccsdt[k-1]=tmp
                tmp=all_opti[k]
                all_opti[k]=all_opti[k-1]
                all_opti[k-1]=tmp
                tmp=all_normal[k]
                all_normal[k]=all_normal[k-1]
                all_normal[k-1]=tmp
                tmp=all_freq[k]
                all_freq[k]=all_freq[k-1]
                all_freq[k-1]=tmp
                tmp=all_charge[k]
                all_charge[k]=all_charge[k-1]
                all_charge[k-1]=tmp
                tmp=all_multi[k]
                all_multi[k]=all_multi[k-1]
                all_multi[k-1]=tmp
                tmp=all_functional[k]
                all_functional[k]=all_functional[k-1]
                all_functional[k-1]=tmp
                tmp=all_bases[k]
                all_bases[k]=all_bases[k-1]
                all_bases[k-1]=tmp
                #
                tmp=all_iscf[k]
                all_iscf[k]=all_iscf[k-1]
                all_iscf[k-1]=tmp
                
#sys.exit()

    iii=1
    suma=0.0
    ciclo=[]
    for i in range(0,len(all_files)):
        delta_i=0.0
        delta_i=(all_energy_scf[i]-all_energy_scf[0])*hartree2kcalmol
        filename=all_files[i]
        charge=int(all_charge[i])
        multi=int(all_multi[i])
        norm=int(all_normal[i])
        fr=int(all_freq[i])
        #istr=str(i+1).zfill(4) 
        funcional1=all_functional[i]
        bases1=all_bases[i]
        iscf1=all_iscf[i]
        if normal_input == "all":
            istr=str(iii).zfill(4) 
            print "%s %30s %16.9f %5d %5d %5d %5d %15s %15s" % (istr,filename,delta_i,charge,multi,norm,fr,funcional1,bases1)
            iii=iii+1
            suma=suma+float(iscf1)
            ciclo.append(iscf1)
        if normal_input == "2" and norm == 2:
            istr=str(iii).zfill(4) 
            print "%s %30s %16.9f %5d %5d %5d %5d %15s %15s" % (istr,filename,delta_i,charge,multi,norm,fr,funcional1,bases1)
            iii=iii+1
            suma=suma+float(iscf1)
            ciclo.append(iscf1)
        if normal_input == "1" and norm == 1:
            istr=str(iii).zfill(4) 
            print "%s %30s %16.9f %5d %5d %5d %5d %15s %15s %15s" % (istr,filename,delta_i,charge,multi,norm,fr,funcional1,bases1,iscf1)
                                                                     
            iii=iii+1
            suma=suma+float(iscf1)
            ciclo.append(iscf1)
                                                                     
        if normal_input == "0" and norm == 0:
            istr=str(iii).zfill(4) 
            print "%s %30s %16.9f %5d %5d %5d %5d %15s %15s %15s" % (istr,filename,delta_i,charge,multi,norm,fr,funcional1,bases1,iscf1)
            iii=iii+1
            suma=suma+float(iscf1)
            ciclo.append(iscf1)
           
    print "--------------------------------------------------------------------------------"

    #promedio=float(suma)/float(iii)
    #print "Average convergence steps=",promedio,max(ciclo),min(ciclo)
    
    #output_geo="salida.molden"
    output_geo=output
    #geo=open(output_geo,"w")
    print "Getting geometry from gaussian outputs ..."
    imole=0
    kkk=1
    mol_from_out={}
    for i in range(0,len(all_files)):
        printer0=0
        norm=int(all_normal[i])
        if normal_input == "all":
            printer0=1
            imole+=1
        if normal_input == "2" and norm == 2:
            printer0=1
            imole+=1
        if normal_input == "1" and norm == 1:
            printer0=1
            imole+=1
        if normal_input == "0" and norm == 0:
            printer0=1
            imole+=1
            
        if printer0 == 1:
            delta_i=0.0
            delta_i=(all_energy_scf[i]-all_energy_scf[0])*hartree2kcalmol
            filename=all_files[i]
            #istr=str(i).zfill(4)
            #print istr,"  ",filename
            #stdout.write("\r%d" % i)
            #fils="File="+istr
            #stdout.write("\r%s" % (istr))
            #stdout.write("\r%s" % (fils))
            #stdout.flush()
            #print "====================================================================="
            gauss=open(filename,'r')
            atoms, coord, vibfreq, vibmode = [], [], [], []
            n_atoms=0
            for line in gauss: 
                if line.strip() in ("Input orientation:", "Standard orientation:"): 
                    for ii in range(4): gauss.next()
                    line=gauss.next()
                    n_atoms=0
                    atoms=[]
                    coordx=[]
                    coordy=[]
                    coordz=[]
                    while not line.startswith(" --------"):
                        ls = line.split()
                        if (len(ls) == 6 and ls[0].isdigit() and ls[1].isdigit() and ls[2].isdigit()):
                            atoms.append(int(ls[1]))
                            coordx.append(float(ls[3]))
                            coordy.append(float(ls[4]))
                            coordz.append(float(ls[5]))
                            #print " ii ",n_atoms, line
                            n_atoms=n_atoms+1
                        else:
                            break
                        line=gauss.next()
            if n_atoms > 0:
                #print >>geo,"%-6d" % (n_atoms)
                #print  "%-6d" % (n_atoms)
                #print kkk,0,6,n_atoms
                #print >>geo,"%-16.9f %s %s" % (delta_i,"  ",filename)
                mol_from_out[kkk,0,6]=n_atoms
                mol_from_out[kkk,0,5]=filename
                mol_from_out[kkk,0,4]=delta_i
                for k in range(0,len(atoms)):
                    symbol='C'
                    if is_number(atoms[k]):
                        symbol=get_chemical_symbols(int(atoms[k]))
                    #print >>geo,"%-2s %16.9f %16.9f %16.9f" % (symbol,coordx[k],coordy[k],coordz[k])
                    mol_from_out[kkk,k,0]=symbol
                    mol_from_out[kkk,k,1]=coordx[k]
                    mol_from_out[kkk,k,2]=coordy[k]
                    mol_from_out[kkk,k,3]=coordz[k]
                kkk+=1
                

    print "Number of molecules=",imole  
    #print "Output=",output_geo
    #geo.close()
    return mol_from_out
