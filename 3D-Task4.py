import numpy.random as nr
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

'''
This program is essentially the same as 2D-Task4.py except that it has been slightly modified to work with spheres. 
The graphical output has also been modified as it doesn't vary between two patterns of colors ( the multicoloured pattern was too confusing). 
The percolating cluster is marked in silver.
Refer to the descriptions made in 2D-Task4.py if needed.
'''
N = 800			# Number of spheres to be simulated
r = 0.05			# Radius

'''
As patches were not available to scatter spheres, the size of the spheres in the graphical output had to be set by the 'markersize' kwarg which 
is in units of points^2. Markersize is therefore the surface area of the spheres. Conversion factors are introduced to change from points to cm.
'''
markersize = 4*np.pi*(r*7*720/25.4)**2		 #!!! I have to use the diameter instead of the radius ???to get the correct area ....

R = nr.uniform(size=(N, 3))								
x = R[:,0]
y = R[:,1]
z = R[:,2]

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
    

def findclusters(array, r) :
	isolatedspheres = {'spheres':[]}
	Bigclusterslist = []

	for i in range(len(array)) :										
		a = overlapdetector(i)
		if a == [] :													
			isolatedspheres['spheres'].append(i)								
		
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

	print "Cluster of the isolated spheres:"
	print isolatedspheres
	print "All other clusters:"
	for cluster in Bigclusterslist :
		print    str(cluster).rjust(0)
	
	# Plotting and Coloring
	fig = plt.figure(figsize =(14,10))									
	ax = fig.add_subplot(1, 1, 1, aspect='equal', projection='3d') 			
	ax.set_xlim([0, 1])
	ax.set_ylim([0, 1])
	ax.set_zlim([0, 1])
	ax.set_xlabel('$percolation \, along \, x$')
	ax.set_ylabel('$y$')
	ax.set_zlabel('$z$')
	plt.title('$3D \, Percolation$')

	for sphereindex in isolatedspheres['spheres'] : 
		ax.scatter(x[sphereindex], y[sphereindex],z[sphereindex], s=markersize, marker='o', color="LightGoldenrodYellow", edgecolors = 'k',  alpha = 0.2)	
	for element in Bigclusterslist :
		for sphereindex in element['spheres'] :
			if element['left'] == True and element['right'] == True :
				ax.scatter(x[sphereindex], y[sphereindex],z[sphereindex], s=markersize, marker='o', color="Silver", edgecolors='k', alpha=0.6)
			else :
				ax.scatter(x[sphereindex], y[sphereindex],z[sphereindex], s=markersize, marker='o', color="LightGoldenrodYellow", edgecolors='grey', alpha = 0.2)


	

findclusters(R,r)
plt.show()








