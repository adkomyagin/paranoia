import numpy
import random
import math

# returns the L2 distance between hist1 and hist2
# assumes hist1 and hist2 have the same number of bins defined by bin_edges
def L2(hist1,hist2,bin_edges):
	sum = 0
	for i in range(0,len(hist1)):
		a = hist1[i] * (bin_edges[i+1] - bin_edges[i])
		b = hist2[i] * (bin_edges[i+1] - bin_edges[i])
		sum += (a-b)**2
	return math.sqrt(sum)

# returns the Jeffries-Matusita distance between hist1 and hist2
# assumes hist1 and hist2 have the same number of bins defined by bin_edges
def JM(hist1,hist2,bin_edges):
	sum = 0
	for i in range(0,len(hist1)):
		a = hist1[i] * (bin_edges[i+1] - bin_edges[i])
		b = hist2[i] * (bin_edges[i+1] - bin_edges[i])
		sum += (math.sqrt(a)-math.sqrt(b))**2
	return math.sqrt(sum)

# returns a random sublist by sampling with replacemnt
def random_sublist(data,size):
	res = []
	for i in range(0,size):
		res.append(random.choice(data))
	return res

# computes the L2 and JM distances for given data sets and the number of bins
def distance_compute(data1,data2,bin_edges):
	hist1, bin_edges = numpy.histogram(data1,bins=bin_edges,density=True)
	hist2 = numpy.histogram(data2,bins=bin_edges,density=True)[0]

	l2 = L2(hist1, hist2, bin_edges)
	jm = JM(hist1, hist2, bin_edges)
	return (l2,jm)

# returns the array of bins
def get_bins(data1,data2,min_step):
        bins = []
        num = int(math.ceil(2* (len(data1) ** (1 / 3.0))));
        max1 = max(data1)
        min1 = min(data1)
        max2 = max(data2)
        min2 = min(data2)
        # print "Min1: " + str(min1) + ", Max1: " + str(max1) + ", Min2: " + str(min2) + ", Max2: " + str(max2)
        # Override num if it's too precise
        num_max = int(math.ceil(float(max1 - min1)/min_step))
        # print "Num: " + str(num) + ", Max: " + str(num_max)
        num = min(num, num_max)
        step = float(max1 - min1)/num
        for i in range(0,num+1):
            bins.append(min1 + i*step)
        # Add data2 boundaries if needed
        #if min2 < min1:
        #    bins.insert(0,min2)
        #if max2 > max1:
        #    bins.append(max2)
        return bins

#------- initial data ------
#data1 = []
#data2 = []
#n = 1000
#
#for i in range(0,n):
#   data1.append(random.gauss(0.005,0.0003))
#
#for i in range(0,n):
#   data2.append(random.gauss(0.005,0.0003))

MIN_STEP = 0.002

data1 = [float(line.strip()) for line in open("s2data1.txt", 'r')]
data2 = [float(line.strip()) for line in open("s2data0.txt", 'r')]

n1 = len(data1)
n2 = len(data2)

assert n1 == n2

n = n1
 
#------- end of initial data ------


#------- true calculation ------
#num_bins = 10 # math.ceil(2* (n ** (1 / 3.0)));
#print "Got " + str(n) + " measurments. Using " + str(num_bins) + " bins"
bin_edges = get_bins(data1,data2,MIN_STEP)
print "Got " + str(n) + " measurments. Using " + str(len(bin_edges)) + " bins"

hist1, bin_edges = numpy.histogram(data1,bins=bin_edges,density=True)

print "Original:"
print hist1
print bin_edges

print numpy.sum(hist1*numpy.diff(bin_edges))

hist2, bin_edges_new = numpy.histogram(data2,bins=bin_edges,density=True)

print "New:"
print hist2
print bin_edges_new

print numpy.sum(hist2*numpy.diff(bin_edges))

# compute L2
l2_true = L2(hist1, hist2, bin_edges)
print "True L2: " + str(l2_true)

# compute JM
jm_true = JM(hist1, hist2, bin_edges)
print "True JM: " + str(jm_true)

#------- end of true calculation ------

#----- bootstrapping start ---------

counter_l2 = 0
counter_jm = 0

for i in range(0,5000):
	data_concat = data1 + data2
	x_data1 = random_sublist(data_concat, len(data1))
	x_data2 = random_sublist(data_concat, len(data2))
        bin_edges = get_bins(x_data1,x_data2,MIN_STEP)
	x_l2, x_jm = distance_compute(x_data1, x_data2, bin_edges)
	if x_l2 > l2_true: counter_l2 = counter_l2 + 1
	if x_jm > jm_true: counter_jm = counter_jm + 1 
	if (i%500 == 0): print str(i/50) + "% done"

#----- bootstrapping end ---------


#------- results evaluation ---
print "L2 Counter: " + str(counter_l2)
print "JM Counter: " + str(counter_jm) 

l2_pass = (counter_l2/5000.0) > 0.05
jm_pass = (counter_jm/5000.0) > 0.05
print "L2 Pass: " + str(l2_pass)
print "JM Pass: " + str(jm_pass)

#------- end of results evaluation ---
