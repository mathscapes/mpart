import time
import datetime
import random
import sys



from visualization import *

import xyPlot
#import xyData

start = time.time()
print("TIME STAMP " + str(datetime.datetime.now()))

myViewport = session.Viewport(name='myViewport', origin=(10, 10), width=300, height=150)

pltname = 'Plot' + str(random.randint(0,124))

xyp = session.XYPlot(name=pltname)			# Ideally, this command must only run once, but by using randint(), everytime a unique plotname is created to resolve the issue.  

chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
chart.legend.setValues(show=True)

mod = ['JB-CP2v250', 'JB-QI2v250', 'JB-QH1v250', 'JB-FT2v250', 'JB-FT2Rv250', 'JB-FY1Rv250', 'JB-FH1v250'] 		# List of job names 
modname = ['CP2', 'QI2', 'QH1', 'FT2', 'FT2R', 'FY1R', 'FH1'] 				# list of curve names to be used in Legends corresponding to Jobs. 

ck = []

for i in range (0,len(mod)):

	myOdb = openOdb(path= mod[i] + '.odb')
	session.viewports['myViewport'].setValues(displayedObject=myOdb)
	session.viewports['myViewport'].restore()
	session.viewports['myViewport'].makeCurrent()
	session.viewports['myViewport'].maximize()
	
# PLotting 

	#xy1=(myOdb.steps['Step-1'].historyRegions['Node PROJ-1.291'].historyOutputs['V3'].data)   # Either use this if you have historyOutputs enabled or use xyDataListFromField method.
	odb = myOdb
	 
	f = session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('V', NODAL, ((COMPONENT, 'V3'), )), ), nodeSets=('PROJ-1.RP', ))
	Disp = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('U', NODAL, ((COMPONENT, 'U3'), )), ), nodeSets=('PROJ-1.RP', ))
		
	XYData(f[0]).save()
	XYData(Disp[0]).save()
	
	comb = combine(Disp[0],f[0])			# can be commented and both plots can be generated separately. Operation of XY data - Combine function to generate - Velocity-Displacement curves. 
	XYData(comb).save()

	#session.xyDataObjects.changeKey(fromName='XYData-1', toName=mod[i])		# use this to rename your saved XYData

	c1 = session.Curve(xyData=comb)
	c1.lineStyle.setValues(thickness=0.5)
	#c1.symbolStyle.setValues(show = True)
	#c1.symbolStyle.setValues(size = 2)
	c1.setValues(legendLabel=modname[i])
	ck.append(c1)
	
	myOdb.close()

chart.setValues(curvesToPlot=(ck ), )
myViewport.setValues(displayedObject=xyp)
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]


print("TIME STAMP " + str(datetime.datetime.now()))