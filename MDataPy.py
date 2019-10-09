
#importing abaqus libraries
from part import *
from material import *
from section import *
from optimization import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sVeltch import *
from visualization import *
from connectorBehavior import *



#Settings		
Te = [23, 90, -100]				#Temperature values

#Model Name
Mod = 'Model-1B'
NodeS = 'Node PROJ-1.1103'
Stepname = 'Step-1'
Varb = ['V3', 'U3', 'RF']
Partname = ['PROJ-1']

#Sample list Stacking sequence/Jobs nomenclature
LamN = [ 'CP1', 'CP2', 'CP3', 'CP4', 'QP1', 'QP2', 'AP1', 'AP2', 'AP3', 'AP4']

#modelname = 'Model-1'
j = 0
newfile = open('results.csv','w+')


#Utility Variables
allVels = []
allDisp = []
allF = []
allT0 = []

for v in range (0,1):							#Loop 1 for different Temperatures

	print('Assigning Temperature...')
	impvel = Te[v]
	print(impvel)

	for o in range (3,len(LamN)):				#Loop 2 for different Stacking Sequences/Jobs
		j = j+1
		print('Job No. ' + str(j))
		print('Assigning Laminate Sequence...')
		
		name = LamN[o]

		print('Creating job name...')
		
		tag = 'I'

		jbname = tag + name + '-T' + str(impvel)	#creating Jobname

		print(jbname)

#Opening ODB		
		print("opened")
		newfile.write("\n #OPENED \n")
		newfile.writelines(jbname + "\n")
		odb=openOdb( path= jbname + '.odb')

#Residual velocity, Vr
		Velo = odb.steps['Step-1'].historyRegions[NodeS].historyOutputs[Varb[0]]	
		New = Velo.data[-1][-1]
		New = New/1000	
		print(New)
		allVels.append(New)
		
		T0 = 100
		
#Time taken to reduce velocity to 0
		for g in range(0,len(Kinetic.data)):
			if (Kinetic.data[g][1] <= 0):
				T0 = Kinetic.data[g][0]				
				break
		print(T0)	
		allT0.append(T0)
		
#Displacement
		Disp = odb.steps[Stepname].historyRegions[NodeS].historyOutputs[Varb[1]].data		
		c = []
		for i in range (0,len(Disp)):
			c.append(Disp[i][1])
			
		MaxDisp = max(c)
		allDisp.append(max(c))		
		print(MaxDisp)
		
#Force
		ns = odb.rootAssembly.instances[Partname].nodeSets['RP']

		dat = []
		for k in range (0,len(odb.steps[Stepname].frames)):

			Frames = odb.steps[Stepname].frames[k].fieldOutputs[Varb[2]]

			jk = Frames.getSubset(region=ns)

			for i in jk.values:
				fp=i.magnitude
				dat.append(fp)
		
			Fmax = max(dat)		
		
		allF.append(Fmax)
		print(Fmax)
		

#Printing
		newfile.writelines(str(New) + "\n")
		newfile.writelines(str(MaxDisp) + "\n")
		newfile.writelines(str(Fmax) + "\n")
		newfile.writelines(str(T0) + "\n")
		odb.close()
		
		
		print('Job Completed')
	
	print('Velocity Set Completed')
	
#Print all
newfile.write("\n")
newfile.write(str(allVels) + "\n")
newfile.write(str(allF) + "\n")
newfile.write(str(allT0) + "\n")
newfile.write(str(allDisp))
newfile.close()