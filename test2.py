import test

data1 = [float(line.strip()) for line in open("s2data1.txt", 'r')]
data2 = [float(line.strip()) for line in open("s2data0.txt", 'r')]

print test.compare_distributions(data1,data2,True)

