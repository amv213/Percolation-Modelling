import numpy.random as nr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

N = 150					 # Number of disks to be simulated						
r = 0.05					# Radius of disks
R = nr.uniform(size=(N, 2))

def overlapdetector(diskindex):	
	'''
	Takes the index of one disk as argument.
	Detects which disks overlap with the given disk and returns a list containing them.
	'''
	distances = abs(R - R[diskindex])				
	xdistances = distances[:,0]					
	ydistances = distances[:,1]
	pythagoradistances = np.sqrt(np.square(xdistances)+np.square(ydistances))  
	overlappingdisks = [ (i) for i in range(len(distances)) if (pythagoradistances[i] <= 2*r and pythagoradistances[i] != 0) ]
	return overlappingdisks
	
def joincluster(c1,c2) :
	'''
	Takes two clusters as arguments ( clusters as dictionaries with a 'disks','left' and 'right' key ).
	Amalgamates the second cluster into the first. Returns the amalgamated cluster.
	'''
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
	'''
	Teakes a list containing clusters and the index of one disk.
	Tells to which cluster/s the disk belongs to.
	'''
	thiscluster = [cluster for cluster in clusterslist if diskindex in cluster['disks']]		
	return thiscluster
	
def touchingdetector(cluster) :                                    
	'''
	Takes a cluster as argument.
	Assigns Boolean values to its 'left' and 'right' keys depending on whether the cluster is touching one or the other edge of the lattice.
	'''
	array = R                                                           
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

def findclusters(array) :
	'''
	This function takes the array containing the positions of all of the disks as arguments and sorts them into clusters.
	It will return a list (isolateddisks) containing all of the isolated disks and a list (Bigclusterslist) containing all of the other clusters.
	Referring to the flowchart of Figure 2 in the report will help in the understanding of this algoithm.
	The graphical output depends wether a percolating cluster is found. If there is a percolating cluster it will be marked in red and all other clusters
	will be in blue. If there is not a percolating cluster all clusters will be colored with a different color in order to easily distinguish them.
	'''
	isolateddisks = {'disks':[]}
	Bigclusterslist = []

	for i in range(len(array)) :										
		a = overlapdetector(i)
		if a == [] :													
			isolateddisks['disks'].append(i)								
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
			else:
				Bigclusterslist.remove(c[0])
				Bigclusterslist.remove(c[1])
				d = joincluster(c[0],c[1])
				if i not in d['disks'] :
					d['disks'].append(i)
				cluster = d
			touchingdetector(cluster)
			Bigclusterslist.append(cluster)
	print "Cluster of the isolated disks:"
	print isolateddisks
	print "All other clusters:"
	for cluster in Bigclusterslist :
		print    str(cluster).rjust(0)
	
	# Plotting and Coloring
	fig = plt.figure()									
	ax = fig.add_subplot(1, 1, 1, aspect='equal') 
	
	RedBlue = None
	for cluster in Bigclusterslist:
		if cluster['right'] == True and cluster['left'] == True :
			RedBlue = True
	
	if RedBlue == True :	
		for diskindex in isolateddisks['disks'] : 
			ax.add_artist(Circle(xy=(array[diskindex]), radius=r, color = 'k', alpha=0.3))	
		for element in Bigclusterslist :
			for diskindex in element['disks'] :
				if element['left'] == True and element['right'] == True :
					ax.add_artist(Circle(xy=(array[diskindex]), radius=r, color = 'r',alpha=0.3))
				else :
					ax.add_artist(Circle(xy=(array[diskindex]), radius=r, color = 'b',  alpha=0.3))
	else:
		colorlist = ['SteelBlue', 'OrangeRed', 'ForestGreen', 'Gold', 'BlueViolet', 'Teal', 'DarkOrange', 'SkyBlue', 'Orchid', 'HotPink', 'Tomato', 'LimeGreen']
		for i in range(len(Bigclusterslist)):
			for diskindex in Bigclusterslist[i]['disks'] : 
				ax.add_artist(Circle(xy=(array[diskindex]), radius=r, color = colorlist[i%len(colorlist)], alpha=0.6))
		for diskindex in isolateddisks['disks'] : 
				ax.add_artist(Circle(xy=(array[diskindex]), radius=r, color = 'k', alpha=0.3))
	plt.show()


findclusters(R)








