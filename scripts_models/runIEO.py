import random
import sys
import os
import xml.etree.ElementTree as et
import numpy as np

# Constants
JMTPATH = '~/JMT/JMT-1.0.5.jar'
PATTERNNAME = 'IsEverythingOK'
SOURCEFILE = 'device-server-' + PATTERNNAME + '.placeholder.jsimg'
NUM_CUSTOMERS_CL1 = 10
NUM_CUSTOMERS_AP = [10]
RESULTS_DIR = 'results/N' + str(NUM_CUSTOMERS_CL1) + '_' + PATTERNNAME + '/'
ATTRIBUTE_NAME = ['num_CL1', 'num_AP', 'IEO_interval', 'S_d1', 'S_dAP', 'S_s1', 'mean', 'lower', 'upper']
SERVICE_DEVICE_CL1 = [0.02]
SERVICE_DEVICE_AP = [0.001]
SERVICE_SERVER_CL1 = [0.04]
SERVICE_SERVER_AP = 0
WAIT_INTERVAL = [0.00001] + list(np.arange(0.001, 0.04, 0.001))


# Print iterations progress
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def generateFileNames(sourcefile):
	tmp = sourcefile.split('.')
	newfile = tmp[0] + '.' + tmp[2] #Remove "placeholder" from the name
	resultname = tmp[0] + '.' + tmp[2] + '-result.jsim'
	return newfile, resultname


def replace_placeholder(sourcefile, targetfile, plcList, subList):
	with open(sourcefile, 'r') as f:
		newText = f.read()
		for plc, sub in zip(plcList, subList):
			newText = newText.replace(str(plc), str(sub))

	with open(targetfile, "w") as f:
	    f.write(newText)


def collectResults(filename, params):
	tree = et.parse(filename)
	root = tree.getroot()
	strParams = ''
	for p in params:
		strParams += str(p)
		strParams += ','
	for measure in root:
		dictAttrib = measure.attrib
		targetname = dictAttrib['station'].replace(' ', '') + '_' + dictAttrib['measureType'].replace(' ', '') + '.csv'
		with open(targetname, 'a') as f:
			if os.stat(targetname).st_size == 0:
				strAttr = ''
				for attr in ATTRIBUTE_NAME:
					strAttr += attr
					strAttr += ','
				f.write(strAttr + '\n')
			f.write(strParams + dictAttrib['meanValue'] + ',' + dictAttrib['lowerLimit'] + ',' + dictAttrib['upperLimit'] + '\n')
		


#################################################


newfile, resultname = generateFileNames(SOURCEFILE)


rate_device_cl1 = [1/s for s in SERVICE_DEVICE_CL1] #placeholder = 111111
rate_device_AP = [1/s for s in SERVICE_DEVICE_AP] #placeholder = 222222 #Antipattern overhead
rate_server_cl1 = [1/s for s in SERVICE_SERVER_CL1] #placeholder = 333333


count = 0
total = len(SERVICE_DEVICE_AP) * len(SERVICE_DEVICE_CL1) * len(SERVICE_SERVER_CL1) * len(NUM_CUSTOMERS_AP) * len(WAIT_INTERVAL)
for num in NUM_CUSTOMERS_AP:
	for wait in WAIT_INTERVAL:
		for r_dAP in rate_device_AP:
			for r_d1 in rate_device_cl1:
				for r_s1 in rate_server_cl1:
					count += 1
					params = [NUM_CUSTOMERS_CL1, num, wait, r_d1, r_dAP, r_s1]
					replace_placeholder(SOURCEFILE, newfile, ['VAL'+str(i) for i in range(len(params))], params)
					cmd = 'java -cp ' + JMTPATH + ' jmt.commandline.Jmt sim ' + newfile
					rnd = str(random.randint(0, sys.maxsize))
					os.popen('java -cp ' + JMTPATH + ' jmt.commandline.Jmt sim ' + newfile + ' -seed ' + rnd).read()
					collectResults(resultname, [x if params.index(x) < len(params)-3 else 1/x for x in params])
					printProgressBar(count, total, prefix = 'Simulating', suffix = 'Completed', length = 50)

os.popen('rm ' + newfile + ' ' + resultname)
if not os.path.isdir('results/'):
	os.popen('mkdir results/')
	os.popen('sleep 3') #TODO: Fix this, it should wait the previous operation to complete, not sleep like this
if not os.path.isdir(RESULTS_DIR):
	os.popen('mkdir ' + RESULTS_DIR)
	os.popen('sleep 3') #TODO: Fix this, it should wait the previous operation to complete, not sleep like this
os.popen('mv *.csv ' + RESULTS_DIR)
