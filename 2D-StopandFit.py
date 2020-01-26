import numpy.random as nr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import scipy as sp
import scipy.optimize as spo
import pylab as pl

'''
The first part of this program is exactly the same as program 2D-Task4.py. The "findclusters" function has simply been modified into a 
"findspanningcluster" function which stops as soon as it finds a percolating cluster. A whole section of program has been added to estimate the 
percolation threshold of the system."
'''
N = 4000 				



def overlapdetector(diskindex):								

	distances = abs(R - R[diskindex])				
	xdistances = distances[:,0]					
	ydistances = distances[:,1]
	pythagoradistances = np.sqrt(np.square(xdistances)+np.square(ydistances))  
	overlappingdisks = [ (i) for i in range(len(distances)) if (pythagoradistances[i] <= 2*r and pythagoradistances[i] != 0) ]
	return overlappingdisks

	
def joincluster(c1,c2) :												
	for element in c2['disks'] :
		if element not in c1['disks'] :									
			c1['disks'].append(element)							
	if c2['left'] == True or c1['left'] == True :							
		c1['left'] = True
	if c2['right'] == True or c1['right'] == True :							
		c1['right'] = True
	c1['disks'].sort()
	return c1

def whichcluster(clusterslist, diskindex) :									
	thiscluster = [cluster for cluster in clusterslist if diskindex in cluster['disks']]		
	return thiscluster
	

def touchingdetector(cluster) :                                     # Assigns the edge truth values to the cluster
          array = R                                                           # looks in the cluster if disks are touching one of the edges
          xcoordinatearray = array[:,0]	
    
          for diskindex in cluster['disks'] :						
                    if xcoordinatearray[diskindex] <= r :					
                              cluster['left'] = True							
                              break										
                    else :										
                              cluster['left'] = False							
          for diskindex in cluster['disks'] :					
                    if xcoordinatearray[diskindex] >= (1-r) :
                              cluster['right'] = True
                              break
                    else :
                              cluster['right'] = False
    

def findspanningcluster(array, r) :
    '''
    This is almost the same function as the 'findclusters' function in 2D-Task4.py. 
    It has been modified to stop as soon as it finds a spanning cluster and returns the disk reached.
    '''
    isolateddisks = {'disks':[]}
    Bigclusterslist = []
          
    for i in range(len(array)) :										
        a = overlapdetector(i)
        if a == [] :													
            isolateddisks['disks'].append(i)								
            if array[i][0] <= r and array[i][0] >= (1-r) :
                return i+1

	else :													
		samplecluster = {'disks':[] , 'left' : None , 'right': None}
		overlappingclusterslist = []
		for disk in a :												
			b =whichcluster(Bigclusterslist, disk)								
			overlappingclusterslist.extend(cluster for cluster in b if cluster not in overlappingclusterslist)
		c = overlappingclusterslist					
		if c == [] :													
			samplecluster['disks'].append(i)
			cluster = samplecluster									
		elif len(c) == 1 :										
			Bigclusterslist.remove(c[0])
			if i not in c[0]['disks'] :
				c[0]['disks'].append(i)
			cluster = c[0]
		else :
			Bigclusterslist.remove(c[0])
			Bigclusterslist.remove(c[1])
			d = joincluster(c[0],c[1])
			if i not in d['disks'] :
				d['disks'].append(i)
			cluster = d
		touchingdetector(cluster)
		Bigclusterslist.append(cluster)
		if cluster['right'] == True and cluster['left'] == True :
			return i+1									# Returns i+1 and not i as the indexes of the disks start from 0 ( 0 being the first disk )


'''
The following section is aimed at calculating the percolation threshold as explained in the report.
'''

radiusrange = np.arange(0.180,0.2,0.0005)			# Range of radii for which we want to find the average number of disks required for percolation
runs = 10									# Number of runs for each radius


'''
This section calculates the average number of disks required for percolation and its erorr for each radius
'''
ydata = []
sigma = []
for r in radiusrange :
	print r								# Print statements are present in order to follow the progress of the programm in the console
	listofpercolatingdisks=[]
	sigma1=[]
	for i in range(runs):
		print i
		R = nr.uniform(size=(N, 2))
		if findspanningcluster(R,r) != None :
			listofpercolatingdisks.append(findspanningcluster(R,r))
	
	averagenumbofdisksforradiusr = sum(listofpercolatingdisks)/len(listofpercolatingdisks)
	print "The estimated percolation treshold for a radius r=", r, " is:", averagenumbofdisksforradiusr
	ydata.append(averagenumbofdisksforradiusr)
	
	yarray = np.array(listofpercolatingdisks)
	sigma1 = np.std(listofpercolatingdisks)/(len(listofpercolatingdisks)**0.5)
	print "with a standard error sigma=", sigma1
	sigma.append(sigma1)



'''
This part is dedicated to fitting the theoretical curve (see report)  to the data and to plot the graph.
The fitting algorithm has been adapted from the model given in the Python worksheets available on Blackboard.
'''

fig = plt.figure()									
ax = fig.add_subplot(1, 1, 1) 

xdata = [i for i in radiusrange]

def fit_func(x,a,c):
   return ((-np.log(1-a))/(np.pi*x*x)) + c
initial_guess=[0.67,1.75]
po,po_cov=spo.curve_fit(fit_func,radiusrange,ydata,initial_guess,sigma)

print "The parameters"
print po
print 'The covariance matrix'
print po_cov
print "So the values with errors are:"
print "phi= ",po[0]," +/- ",sp.sqrt(po_cov[0,0])
print "c= ",po[1]," +/- ",sp.sqrt(po_cov[1,1])

plt.scatter(xdata,ydata, color='LightSteelBlue', marker='o', alpha=0.7, edgecolors='RoyalBlue')
plt.errorbar(xdata, ydata, sigma, 0, capsize=3, ls='None', color='LightSteelBlue')
pl.plot(radiusrange,fit_func(radiusrange,po[0],po[1]),'r-',label='$Fitted \, Curve \, n_c = -\ln(1-\phi_c)/\pi r^2$')

plt.xlabel('$Radius, \, r$', fontsize = 20)
plt.ylabel('$Average \, number \, of \, disks \, for \, spanning \, cluster, \, n_c$', fontsize = 20)
plt.title('$Relationship \, between \, number \, of \, disks \, for \, percolation\, and \, radius$', fontsize = 20)
plt.grid(True)
plt.text(0.5, 0.95,'$\phi_c = %s \pm %s $' %(round(po[0],5),round(sp.sqrt(po_cov[0,0]),5) ), horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=15)
plt.text(0.5, 0.9,'$\eta_c = %s \pm %s $' %(round((-np.log(1-po[0])),5),round((-1/(po[0]-1))*sp.sqrt(po_cov[0,0]),5) ), horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=15)
plt.legend( loc='upper right')
plt.show()