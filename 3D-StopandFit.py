import numpy.random as nr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import scipy as sp
import scipy.optimize as spo
import pylab as pl

'''
This program is the 3D equivalent of 2D-StopandFit.py. The changes made from program 3D-Task4.py and this one are equivalent 
to the changes made from 2D-Task4.py to 2D-StopandFit.py. Refer to those programs if needed.
Thereby this programs stops as soon as it finds a spanningcluster and estimates the percolation threshold of the system.
'''
N = 11000


def overlapdetector(sphereindex):									
	
	distances = abs(R - R[sphereindex])				
	xdistances = distances[:,0]					
	ydistances = distances[:,1]
	zdistances = distances[:,2]
	pythagoradistances = np.sqrt(np.square(xdistances)+np.square(ydistances)+np.square(zdistances))  
	overlappingspheres = [ (i) for i in range(len(distances)) if (pythagoradistances[i] <= 2*r and pythagoradistances[i] != 0) ]
	return overlappingspheres
	
def joincluster(c1,c2) :						
	for element in c2['spheres'] :
		if element not in c1['spheres'] :									
			c1['spheres'].append(element)								
	if c2['left'] == True or c1['left'] == True :							
		c1['left'] = True
	if c2['right'] == True or c1['right'] == True :							
		c1['right'] = True
	c1['spheres'].sort()
	return c1

def whichcluster(clusterslist, sphereindex) :																	
	thiscluster = [cluster for cluster in clusterslist if sphereindex in cluster['spheres']]	
	return thiscluster
	

def touchingdetector(cluster) :                                     
    array = R                                                          
    xcoordinatearray = array[:,0]	
    
    for sphereindex in cluster['spheres'] :						
        if xcoordinatearray[sphereindex] <= r :					
            cluster['left'] = True							
            break										
        else :										
            cluster['left'] = False							
        for sphereindex in cluster['spheres'] :					
            if xcoordinatearray[sphereindex] >= (1-r) :
                cluster['right'] = True
                break
            else :
                cluster['right'] = False
    

def findspanningcluster(array, r) :
	isolatedspheres = {'spheres':[]}
	Bigclusterslist = []

	for i in range(len(array)) :										
		a = overlapdetector(i)
		if a == [] :													
			isolatedspheres['spheres'].append(i)								
			if array[i][0] <= r and array[i][0] >= (1-r) :
				return i+1
		else :													
			samplecluster = {'spheres':[] , 'left' : None , 'right': None}			
			overlappingclusterslist = []
			
			for sphere in a :												
				b =whichcluster(Bigclusterslist, sphere)								
				overlappingclusterslist.extend(cluster for cluster in b if cluster not in overlappingclusterslist)
			
			c = overlappingclusterslist					
			if c == [] :																										
				samplecluster['spheres'].append(i)
				cluster = samplecluster
			elif len(c) == 1 :										
				Bigclusterslist.remove(c[0])
				if i not in c[0]['spheres'] :
					c[0]['spheres'].append(i)
				cluster = c[0]
			else :
				Bigclusterslist.remove(c[0])
				Bigclusterslist.remove(c[1])
				d = joincluster(c[0],c[1])
				if i not in d['spheres'] :
					d['spheres'].append(i)
				cluster = d
			
			touchingdetector(cluster)
			Bigclusterslist.append(cluster)	
			if cluster['right'] == True and cluster['left'] == True :
					return i+1


'''
Section aimed at calculating the percolation threshold as explained in the report.
'''
radiusrange = np.arange(0.18,0.2,0.0005)		# Range of radii for which we want to find the average number of spheres required for percolation
runs = 10								# Number of runs for each radius

'''
This section calculates the average number of spheres required for percolation and its erorr for each radius
'''
ydata = []
sigma = []
for r in radiusrange :
	print r
	percolatingsphere = []
	sigma1=[]
	for i in range(runs):
		print i
		R = nr.uniform(size=(N, 3))							
		percolatingsphere.append(findspanningcluster(R,r))
	listofpercolatingspheres = [element for element in percolatingsphere if element != None]
	
	averagenumbofspheresforradiusr = sum(listofpercolatingspheres)/len(listofpercolatingspheres)
	print "The estimated percolation treshold for a radius r=", r, " is:", averagenumbofspheresforradiusr
	ydata.append(averagenumbofspheresforradiusr)
	
	yarray = np.array(listofpercolatingspheres)
	sigma1 = np.std(listofpercolatingspheres)/(len(listofpercolatingspheres)**0.5)
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
   return ((-3*np.log(1-a))/(np.pi*4.*x*x*x)) + c
initial_guess=[0.3,1.75]
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
pl.plot(radiusrange,fit_func(radiusrange,po[0],po[1]),'r-',label='$Fitted \, Curve \, n_c = -3\ln(1-\phi_c)/4\pi r^3$')
#ax.set_xlim([0,0.20])
plt.xlabel('$Radius, \, r$', fontsize = 20)
plt.ylabel('$Average \, number \, of \, spheres \, for \, spanning \, cluster, \, n_c$', fontsize = 20)
plt.title('$Relationship \, between \, number \, of \, spheres \, for \, percolation \, and \, radius$', fontsize = 20)
plt.grid(True)
plt.text(0.5, 0.95,'$\phi_c = %s \pm %s $' %(round(po[0],5),round(sp.sqrt(po_cov[0,0]),5) ), horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=15)
plt.text(0.5, 0.9,'$\eta_c = %s \pm %s $' %(round((-np.log(1-po[0])),5),round((-1/(po[0]-1))*sp.sqrt(po_cov[0,0]),5) ), horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=15)
plt.legend( loc='upper right')
plt.show()