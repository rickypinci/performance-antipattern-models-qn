# Replication Package: QN-based Modeling and Analysis of Software Performance Antipatterns for Cyber-Physical Systems



This is a replication package for the paper titled "QN-based Modeling and Analysis of Software Performance Antipatterns for Cyber-Physical Systems" and accepted for the 12th ACM/SPEC International Conference on Performance Engineering (ICPE 2021). The pre-print of this paper is publicly available [here](https://cs.gssi.it/catia.trubiani/download/ICPE-2021-perf-antipatt-CPS-preprint.pdf).

## Authors
Riccardo Pinciroli - Gran Sasso Science Institute (Italy)<br/>
Connie U. Smith - Performance Engineering Services (USA)<br/>
Catia Trubiani - Gran Sasso Science Institute (Italy)

## Abstract
Identifying performance problems in modern software systems is nontrivial, even more so when looking at specific application domains, such as cyber-physical systems. The heterogeneity of software and hardware components makes the process of performance evaluation more challenging, and traditional software performance engineering techniques may fail while dealing with interacting and heterogeneous components.
The goal of this paper is to introduce a systematic methodology to understand software performance problems in cyber-physical systems. In our previous work, we listed some common bad practices, namely software performance antipatterns, that may occur. Here we are interested in shedding light on these antipatterns by means of performance models, i.e., queuing network models, that provide evidence of how antipatterns may affect the overall system performance.
Starting from the specification of three software performance antipatterns tailored for cyber-physical systems, we provide the queuing network models capturing the corresponding bad practices. The analysis of these models demonstrates their usefulness in recognizing performance problems early in the software development process. This way, performance engineers are supported in the task of detecting and fixing the performance criticalities.

## Available Files
- *varEnv.py* allows specifying the <tt>JMTPATH</tt> variable (i.e., where the *jar* file of the *Java Modelling Tools* is located) that is used in all the scripts of the package.
- The *script_models/* directory contains files that can be used to plot the same figure as those in the paper. These files are listed in the following.
- Jsimg files contain the model that is simulated using Java Modelling Tools (please, refer to the [Prerequisites](#prerequisites) section below); they should not be modified to avoid that other scripts stop working.
- *runBaseline.py* allows generating data for Figure 3.
- *runAWTY.py* allows generating data for Figure 7(a).
- *runIEO.py* allows generating data for Figure 7(b).
- *runWWI.py* allows generating data for Figure 7(c).
- *analysis_methodology.ipynb* allows plotting Figures 3 and 7.
- *runSensorNet_Baseline.py* allows generating data for Table 6.
- *runSensorNet_AWTY.py* allows generating data for Figure 11.
- *runSensorNet_IEO.py* allows generating data for Figure 12.
- *runSensorNet_WWI.py* allows generating data for Figure 13.
- *analysis_case_study.ipynb* allows generating Table 6 and plotting Figures 11, 12, and 13.
- *runSensorNet.py* allows generating data for any other configuration of the sensor net case study. You can test different configurations by changing variables from line 110 to line 138. Once data are generated, you can use the *analysis_case_study.ipynb* notebook to plot them (after changing the input file).
- *results/* directory comes with all data required to plot Figures 3, 7, 11, 12, and 13 in case you do not want to run all the simulation.

## Prerequisites
This is a list of other tools, libraries, and modules required to reproduce the results of our paper.
- [Java Modelling Tools](http://jmt.sourceforge.net/Download.html) that provides the simulator (JSIMG) used to obtain these results. Scripts in this repository have been tested with the JAR version of JMT 1.0.5
- Python 3
- The following Python modules:
  - Numpy (install with *pip3 install numpy*)
  - Pandas (install with *pip3 install pandas*)
  - Matplotlib (install with *pip3 install matplotlib*)
  - Jupyter (install with *pip3 install notebook*)
- Other Python modules that are in *stdlib* (they do not require to be installed)
  - os
  - sys
  - random
  - xml.etree.ElementTree

## Run a JMT model

### Approach Section
1. Set the <tt>JMTPATH</tt> variable in *varEnv.py* with the PATH of the JMT.jar file.
2. Go to the *script_models/* directory.
3. This directory contains all the scripts you need to generate data and plot figures as those in the paper. Next steps are described using the *runAWTY.py* script as an example. It generates data that are later used for plotting Figure 7(a) of the paper. The same steps must be used to run any other python script in this repository. If you do not want to run all simulations, the *results/* directory already contains all the data required to plot figures shown in the paper (in this case, go to step 8).
4. Save and exit.
5. Run the script using the command: <tt>python runAWTY.py</tt>.
6. When all simulations are completed, results are stored in a *CSV* file inside the *results/* directory.
7. Those data can be used to plot Figure 7(a). Please, open the *analysis_methodology.ipynb* jupyter notebook and run all cells in the *Are We There Yet?* section.


### Case-Study Section
1. Set the <tt>JMTPATH</tt> variable in *varEnv.py* with the PATH of the JMT.jar file.
2. Go to the *script_models/* directory.
3. To simulate sensor nets (i.e., the case-study) using different parameters, you can follow these steps. We use as an example the baseline model (with parameters in Table 5 and results in Table 6 of the paper).
4. Open *runSensorNet.py*.
5. Substitue *TEST_NAME = ''* (line 11) with *TEST_NAME = 'newSim'* (or any other name that you like). Then, save and exit.
6. The parameters used in these scripts allow obtaining the same results shown in the paper. Feel free to change the *Simulation parameters* section of each script to test different system configurations.
7. Use the command <tt>python3 runSensorNet.py sensor_net_closed.placeholder.jsimg</tt> to start the simulation of the case-study.
8. When the simulation is completed, results are stored in a *CSV* file inside the *results/sensor_net_closed_newSim/* directory.
9. Open the jupyter notebook *analysis_case_study.ipynb*.
10. Load the desired data using <tt>pd.read\_csv($filename)</tt>. For example, the content of the second cell can be substituted with: <tt>df = pd.read_csv('results/sensor\_net\_closed\_newSim/sensor\_net\_closed\_collectResults.csv')</tt>.
11. Run the first three cells of the notebook to print the desired results.
