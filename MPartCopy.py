#Scripts for copying parts 

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

modelname = 'Model-1' #can be used to copy from two different models

#Copy command copies everything from property and mesh to section assignments and orientation attributes and more..
#can mesh one object and relay it to other parts with one click

for i in range(2,13):
	pname = 'Plate-'+str(i)						#Part name to copy to
	pold = 'Plate-'+str(i-1)					#Part name to copy from
	
	mdb.models[modelname].Part(name=pname, objectToCopy=
		mdb.models[modelname].parts[pold])
		
