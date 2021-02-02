import random
import os
import time
import xml.etree.ElementTree as et
import numpy as np
import sys
sys.path.insert(1, '../')
from varEnv import *

# Constants
#JMTPATH = '~/JMT/JMT-1.0.5.jar'
PATTERNNAME = ''
TEST_NAME = ''
MODEL_NAME = 'sensor_net_closed'
SOURCEFILE = MODEL_NAME + PATTERNNAME + '.placeholder.jsimg'
if PATTERNNAME != '':
	PATTERNNAME = '_' + PATTERNNAME
if TEST_NAME != '':
	RESULTS_DIR = 'results/' + MODEL_NAME + PATTERNNAME + '_' + TEST_NAME + '/'
else:
	RESULTS_DIR = 'results/' + MODEL_NAME + PATTERNNAME + '_' + str(int(time.time())) + '/'
PARAM_NAME = [
'num_polling', #integer
'num_status', #integer
'num_actor', #integer
'num_data', #integer
'Z_polling',
'Z_status', #Deterministic
'Z_actor',
'S_ctrl_polling',
'S_ctrl_analysis',
'S_ctrl_status',
'S_ctrl_exception',
'S_ctrl_actor',
'num_server_ctrl', #integer
'S_db_analysis',
'S_db_actor',
'S_sensors_status',
'Z_data',
'prob_status_exception', #prob
'prob_status_status' #1-prob
]
INDEX_NAME = [
'Xctrl_polling_mean',
'Xctrl_polling_low',
'Xctrl_polling_up',
'Xctrl_analysis_mean',
'Xctrl_analysis_low',
'Xctrl_analysis_up',
'Xctrl_status_mean',
'Xctrl_status_low',
'Xctrl_status_up',
'Xctrl_exception_mean',
'Xctrl_exception_low',
'Xctrl_exception_up',
'Xctrl_actor_mean',
'Xctrl_actor_low',
'Xctrl_actor_up',
'XgenData_data_mean',
'XgenData_data_low',
'XgenData_data_up',
'Rctrl_polling_mean',
'Rctrl_polling_low',
'Rctrl_polling_up',
'Rctrl_analysis_mean',
'Rctrl_analysis_low',
'Rctrl_analysis_up',
'Rdb_analysis_mean',
'Rdb_analysis_low',
'Rdb_analysis_up',
'Rctrl_status_mean',
'Rctrl_status_low',
'Rctrl_status_up',
'Rsensors_status_mean',
'Rsensors_status_low',
'Rsensors_status_up',
'Rctrl_exception_mean',
'Rctrl_exception_low',
'Rctrl_exception_up',
'Rctrl_actor_mean',
'Rctrl_actor_low',
'Rctrl_actor_up',
'Rdb_actor_mean',
'Rdb_actor_low',
'Rdb_actor_up',
'Uctrl_polling_mean',
'Uctrl_polling_low',
'Uctrl_polling_up',
'Uctrl_analysis_mean',
'Uctrl_analysis_low',
'Uctrl_analysis_up',
'Uctrl_status_mean',
'Uctrl_status_low',
'Uctrl_status_up',
'Uctrl_exception_mean',
'Uctrl_exception_low',
'Uctrl_exception_up',
'Uctrl_actor_mean',
'Uctrl_actor_low',
'Uctrl_actor_up',
]
ATTRIBUTE_NAME = PARAM_NAME + INDEX_NAME
NUM_PARAM_VALS = len(PARAM_NAME)
NUM_INDEX_VALS = len(INDEX_NAME)
NUM_TOTAL_VALS = len(ATTRIBUTE_NAME)
#Prepare the header of the CSV file (i.e., attribute names)
ATTRIBUTE_STR = ''
for attr in ATTRIBUTE_NAME:
	ATTRIBUTE_STR += attr + ','
ATTRIBUTE_STR = ATTRIBUTE_STR[:-1]

#####################################################################################
#####################################################################################
############################ START: Simulation parameters ###########################
#####################################################################################
#####################################################################################
###### Number of customers for each class ######
N_POLLING = [1]
N_STATUS = [1]
N_ACTOR = [5]
N_DATA = [8]
###### Think times at the delay station ######
Z_POLLING = [0.0001] #Exponential
Z_STATUS = [0.0001] #Deterministic, cannot be 0
Z_ACTOR = [0.03] #Exponential
Z_DATA = [0.06] #Exponential (in the generateData station)
#Analysis and Exception spend 0 time units in the delay
###### Number of servers for the controller ######
NUM_CTRL_SERVERS = [2]
###### Service times at the controller ######
S_CTRL_POLLING = [0.0001]
S_CTRL_ANALYSIS = [0.00341]
S_CTRL_STATUS = [0.0001]
S_CTRL_EXCEPTION = [0.005]
S_CTRL_ACTOR = [0.00216]
###### Service times at the DB ######
S_DB_ANALYSIS = [0.0018]
S_DB_ACTOR = [0.0012]
###### Service times at sensors ######
S_SENSORS_STATUS = [0.001]
#Polling, Status, and Exception spend 0 time units in the Cloud station
###### Probability Status to Exception (ClassSwitch1) ######
PROB_STATUS_EXCEPTION = [0.0]
PROB_STATUS_STATUS = [1-x for x in PROB_STATUS_EXCEPTION]
#####################################################################################
#####################################################################################
############################ END: Simulation parameters ###########################
#####################################################################################
#####################################################################################


###### List for collecting measures. This must be specified following the order of ATTRIBUTE_NAME. ['type', 'referenceUserClass', 'station'] ######
collectList = [
['Throughput', 'Polling', 'Controller'],
['Throughput', 'Analysis', 'Controller'],
['Throughput', 'Status', 'Controller'],
['Throughput', 'Exception', 'Controller'],
['Throughput', 'Actors', 'Controller'],
['Throughput', 'sensorData', 'generateData'],
['Response Time', 'Polling', 'Controller'],
['Response Time', 'Analysis', 'Controller'],
['Response Time', 'Analysis', 'Database'],
['Response Time', 'Status', 'Controller'],
['Response Time', 'Status', 'Sensors'],
['Response Time', 'Exception', 'Controller'],
['Response Time', 'Actors', 'Controller'],
['Response Time', 'Actors', 'Database'],
['Utilization', 'Polling', 'Controller'],
['Utilization', 'Analysis', 'Controller'],
['Utilization', 'Status', 'Controller'],
['Utilization', 'Exception', 'Controller'],
['Utilization', 'Actors', 'Controller'],
]


###### Utility functions ######
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
	targetname = tmp[0] + '_collectResults.csv'
	return newfile, resultname, targetname


def replace_placeholder(sourcefile, targetfile, plcList, subList):
	with open(sourcefile, 'r') as f:
		newText = f.read()
		for plc, sub in zip(plcList, subList):
			newText = newText.replace(str(plc), str(sub))

	with open(targetfile, "w") as f:
	    f.write(newText)


def collectResults(filename, targetname, params):
	tree = et.parse(filename)
	root = tree.getroot()
	nextLine = ''
	for p in params:
		nextLine += str(p)
		nextLine += ','
	for l in collectList:
		dictAttrib = root.findall('.//measure[@measureType="'+str(l[0])+'"][@class="'+str(l[1])+'"][@station="'+str(l[2])+'"]')[0].attrib
		nextLine = nextLine + dictAttrib['meanValue'] + ',' + dictAttrib['lowerLimit'] + ',' + dictAttrib['upperLimit'] + ','
	nextLine = nextLine[:-1] #Remove the last comma
	with open(targetname, 'a') as f:
		if os.stat(targetname).st_size == 0:
			f.write(ATTRIBUTE_STR + '\n')
		f.write(nextLine + '\n')		


#################################################


newfile, resultname, targetname = generateFileNames(SOURCEFILE)


rate_delay_polling = [1/x if x > 0 else 'Infinity' for x in Z_POLLING]
rate_delay_actor = [1/x if x > 0 else 'Infinity' for x in Z_ACTOR]
rate_genData_data = [1/x if x > 0 else 'Infinity' for x in Z_DATA]
rate_ctrl_polling = [1/x if x > 0 else 'Infinity' for x in S_CTRL_POLLING]
rate_ctrl_analysis = [1/x if x > 0 else 'Infinity' for x in S_CTRL_ANALYSIS]
rate_ctrl_status = [1/x if x > 0 else 'Infinity' for x in S_CTRL_STATUS]
rate_ctrl_exception = [1/x if x > 0 else 'Infinity' for x in S_CTRL_EXCEPTION]
rate_ctrl_actor = [1/x if x > 0 else 'Infinity' for x in S_CTRL_ACTOR]
rate_db_analysis = [1/x if x > 0 else 'Infinity' for x in S_DB_ANALYSIS]
rate_db_actor = [1/x if x > 0 else 'Infinity' for x in S_DB_ACTOR]
rate_sensors_status = [1/x if x > 0 else 'Infinity' for x in S_SENSORS_STATUS]


count = 0
total = len(N_POLLING) * len(N_STATUS) * len(N_ACTOR) * len(N_DATA) * len(Z_POLLING) * len(Z_STATUS) * len(Z_ACTOR) * len(Z_DATA) * len(S_CTRL_POLLING) * len(S_CTRL_ANALYSIS) * len(S_CTRL_STATUS) * len(S_CTRL_EXCEPTION) * len(S_CTRL_ACTOR) * len(S_SENSORS_STATUS) * len(S_DB_ANALYSIS) * len(S_DB_ACTOR) * len(PROB_STATUS_EXCEPTION) * len(NUM_CTRL_SERVERS)
for nC in NUM_CTRL_SERVERS:
	for np in N_POLLING:
		for ns in N_STATUS:
			for na in N_ACTOR:
				for nd in N_DATA:
					for rdp in rate_delay_polling:
						for kds in Z_STATUS:
							for rda in rate_delay_actor:
								for rgd in rate_genData_data:
									for rcp in rate_ctrl_polling:
										for rcAn in rate_ctrl_analysis:
											for rcs in rate_ctrl_status:
												for rce in rate_ctrl_exception:
													for rca in rate_ctrl_actor:
														for rDBAn in rate_db_analysis:
															for rDBa in rate_db_actor:
																for rss in rate_sensors_status:
																	for p in PROB_STATUS_EXCEPTION:
																		count += 1
																		params = [np, ns, na, nd, rdp, kds, rda, rcp, rcAn, rcs, rce, rca, nC, rDBAn, rDBa, rss, rgd, p, 1-p]
																		replace_placeholder(SOURCEFILE, newfile, ['VAL'+str(i).zfill(2) for i in range(len(params))], params)
																		cmd = 'java -cp ' + JMTPATH + ' jmt.commandline.Jmt sim ' + newfile
																		rndSeed = str(random.randint(0, sys.maxsize)) #Random seed for the simulation
																		os.popen('java -cp ' + JMTPATH + ' jmt.commandline.Jmt sim ' + newfile + ' -seed ' + rndSeed).read()
																		paramsToWrite = [np, ns, na, nd, 1/rdp if rdp != 'Infinity' else 0, kds, 1/rda if rda != 'Infinity' else 0, 1/rcp if rcp != 'Infinity' else 0, 1/rcAn if rcAn != 'Infinity' else 0, 1/rcs if rcs != 'Infinity' else 0, 1/rce if rce != 'Infinity' else 0, 1/rca if rca != 'Infinity' else 0, nC, 1/rDBAn if rDBAn != 'Infinity' else 0, 1/rDBa if rDBa != 'Infinity' else 0, 1/rss if rss != 'Infinity' else 0, 1/rgd if rgd != 'Infinity' else 0, p, 1-p] #Rates are inverted to time (only for writing results)
																		collectResults(resultname, targetname, paramsToWrite)
																		printProgressBar(count, total, prefix = 'Simulating', suffix = 'Completed', length = 50)


os.popen('rm ' + newfile + ' ' + resultname)
if not os.path.isdir('results/'):
	os.popen('mkdir results/')
	os.popen('sleep 3') #TODO: Fix this, it should wait the previous operation to complete, not sleep like this
if not os.path.isdir(RESULTS_DIR):
	os.popen('mkdir ' + RESULTS_DIR)
	os.popen('sleep 3') #TODO: Fix this, it should wait the previous operation to complete, not sleep like this
os.popen('mv *.csv ' + RESULTS_DIR)
