import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math

def compute(bin, oldy, oldx):
	if(~(abs(oldx)<.5 and abs(oldy) <.5)):
		value = round(math.degrees(math.atan2(oldy,oldx)))
		if value < 0:
			value += 360
		#print str(value) + ": value, oldy: " + str(oldy) + ", oldx: " +str(oldx)
		#print "The value is: " + str(value)
		if(~(value <= 120 and value >= 60) and ~(value <= 240 and value >= 300)):
			if (value >270 or value < 90):
				bin[0] += math.sqrt(oldx**2 + oldy**2)
			else:
				bin[1] += math.sqrt(oldx**2 + oldy**2)				
		return bin
	else:
		return bin
	
def createHistogram(bin, frameNum,folder):
	mySum = float(sum(bin))
	if mySum != 0:
		#print str(bin) + " frame: " + str(frameNum)
		#print str(float(max(bin))/float(sum(bin))) + "-> prob of max"
		#weights = np.ones_like(bin)/float(len(bin))	# normalize in order to get a probability
		#n, bins, patches = plt.hist(bin, len(bin), weights=weights,facecolor='green')
		for x in xrange(2):
			bin[x] = float(bin[x])/mySum
			#print x
		if abs(bin[1]-bin[0]) < .6:
			print "stationary"
		elif bin[1]>bin[0]:
			print "left"
		else:
			print "right"
		plt.plot(bin)
		plt.xlabel('Vector in Degrees')
		plt.ylabel('Probability')
		plt.title('Histogram of Frame:' + str(frameNum))
		plt.grid(True)
		plt.axis([0, 2, 0, 1])
		plt.savefig(str(folder) + "/histogram" + str(frameNum))
		plt.clf()
		
####### movement estimates
#frames 1-72 moving left definitely
# frames 73-133 = right
# frames 200-247 = down
# frame 250-335 = up
# frame 450-475 = in
#######
