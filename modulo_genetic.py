####definitions and declarations related to genetic algoriths in general
## metropolis(e0,e1,t)
## get_fitness(fff)

def metropolis(e0,e1,t):
        import math 
        ri=random.uniform(0,1)
        KB=1.38064852e-23
        dE0=e1-e0
        dE=dE0*4.3597e-18
        P=math.exp(-dE/KB*t)
        return (ri,P) 

def get_fitness(fff):
     total_molecules1=(how_many_molecules(fff))
     for imol in range(1,total_molecules1+1):
             Emax=fff[imol,0,4]
     Emin=fff[1,0,4]
     sum_of_fitness=0.0
     for imol in range(1,total_molecules1+1):
            Ei=fff[imol,0,4]
            Fi=(Ei-Emin)/(Emax-Emin)
            fi=0.5*(1-np.tanh(((2.0*Fi)-1)))
            #fi=Fi*100 #exp(-3.0*Fi)
            sum_of_fitness=sum_of_fitness+fi
            #fi=exp(-3.0*Fi)       
     #print sum_of_fitness 
     previous_probability=0.0
     ## rulette w
     ## https://sourcecodebrowser.com/python-biopython/1.58/_roulette_wheel_8py_source.html 
     s=0
     probabilities=[]
     probabilities.append(0.0)
     for imol in range(1,total_molecules1+1):
            Ei=fff[imol,0,4]
            Fi=(Ei-Emin)/(Emax-Emin)
            fi=0.5*(1-np.tanh(((2.0*Fi)-1)))
            pii=(fi/sum_of_fitness)
            previous_probability=previous_probability + (fi/sum_of_fitness) 
            probabilities.append(previous_probability)
            #print "%6.12f %6.12f %6.12f " % (Ei, pii, previous_probability)
     ## rulette wheel selection 
     prev_prob=0.0 
     old=probabilities[0] 
     mmother=[]
     ffather=[] 
     ## here poner el numero de hijos en porcentaje 10% 
     total_hijos=int(ceil((total_molecules1)*0.15))
     #print total_molecules1,total_hijos
     #for iii in range(0,10):
     ##  by hand do a auto-crossover and force to mix the good one with the worst one  
     mmother.append(1)
     ffather.append(1)
     mmother.append(1)
     ffather.append(total_molecules1)
     for iii in range(0,total_hijos):    
       print "------------- Parents -------------- ",iii
       n_idividuos=2
       x_indivi=0
       while x_indivi < n_idividuos:
         jj=1
         rra1 = random.random()
         for cur_prob in range(1,len(probabilities)):
             cur_prob=probabilities[cur_prob]
             if (rra1 >= prev_prob) and (rra1 <= cur_prob):
                 if x_indivi == 0: ## first   mother 
                     mmother.append(jj)
                     print "%5d  %9.6f  %9.6f  %9.6f %s"  % (jj,prev_prob, cur_prob,rra1,"Mother")
                 if x_indivi == 1: ## second  father 
                     ffather.append(jj)
                     print "%5d  %9.6f  %9.6f  %9.6f %s"  % (jj,prev_prob, cur_prob,rra1,"Father")
                 x_indivi+=1
             jj+=1
             prev_prob = cur_prob
     return mmother,ffather
