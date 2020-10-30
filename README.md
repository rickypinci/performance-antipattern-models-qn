# Modeling Performance Antipattern with Queuing Networks
Repository containing all the scripts and models used for modeling Performance Antipatterns with queuing networks

## Run a JMT model
1. Download the [Java Modelling Tools](http://jmt.sourceforge.net/Download.html) (these scripts have been tested with the JAR version of JMT 1.0.5);
2. go to the *jmt_models/* directory;
3. open the Python script of the model that you want to run (e.g., *runSensorNet.py*, same steps work also for other models);
4. set the *JMTPATH* variable (line 9) with the PATH of the JMT.jar file;
3. change values of simulation parameters (from line 110 to line 138), define list of values to run multiple simulations;
4. once you are done, save and exit;
5. run the Sensor Net model with the command: *python runSensorNet.py*;
6. when all simulations are completed, results are stored in a *CSV* file;
7. the *CSV* file can be used to retrieve data and plot results.

## Run a SPEED model
TBD
