# QN-based Modeling and Analysis of Software PerformanceAntipatterns for Cyber-Physical Systems (Repository)
This is a replication package for the paper titled "QN-based Modeling and Analysis of Software PerformanceAntipatterns for Cyber-Physical Systems" and submitted to the 12th ACM/SPEC International Conference on Performance Engineering (ICPE 2021).

## Abstract
Identifying performance problems in modern software systems is nontrivial, even more so when looking at specific application domains, such as cyber-physical systems. The heterogeneity of software and hardware components makes the process of performance evaluation more challenging, and traditional software performance engineering techniques may fail while dealing with interacting and heterogeneous components.
The goal of this paper is to introduce a systematic methodology to understand software performance problems in cyber-physical systems. In our previous work, we listed some common bad practices, namely software performance antipatterns, that may occur. Here we are interested in shedding light on these antipatterns by means of performance models, i.e., queuing network models, that provide evidence of how antipatterns may affect the overall system performance.
Starting from the specification of three software performance antipatterns tailored for cyber-physical systems, we provide the queuing network models capturing the corresponding bad practices. The analysis of these models demonstrates their usefulness in recognizing performance problems early in the software development process. This way, performance engineers are supported in the task of detecting and fixing the performance criticalities.

## Available Files
The *script_models/* directory contains files that can be used to plot the same figure as those in the paper.
- *runBaseline.py* allows generating data for Figure 3
- *runAWTY.py* allows generating data for Figure 7(a)
- *runIEO.py* allows generating data for Figure 7(b)
- *runWWI.py* allows generating data for Figure 7(c)
- *analysis_methodology.ipynb* allows plotting Figures 3 and 7
- *runSensorNet_AWTY.py* allows generating data for Figure 11
- *runSensorNet_IEO.py* allows generating data for Figure 12
- *runSensorNet_WWI.py* allows generating data for Figure 13
- *analysis_case_study.ipynb* allows plotting Figures 11, 12, and 13
- *runSensorNet.py* allows generating data for any other configuration of the sensor net case study. You can test different configurations by changing variables from line 110 to line 138. Once data are generated, you can use the *analysis_case_study.ipynb* notebook to plot them (after having changed the input file).
- *results/* directory comes with all data required to plot Figures 3, 7, 11, 12, and 13 in case you do not want to run all the simulation

## Run a JMT model
1. Download the [Java Modelling Tools](http://jmt.sourceforge.net/Download.html) (these scripts have been tested with the JAR version of JMT 1.0.5).
2. Go to the *script_models/* directory.
3. This directory contains all the scripts you need to generate data and plot figures as those in the paper. Next steps are described using the *runAWTY.py* script as an example. It generates data that are later used for plotting Figure 7(a) of the paper. The same steps must be used to run any other python script in this repository. If you do not want to run all simulations, the *results/* directory already contains all the data required to plot figures shown in the paper (in this case, go to step 9).
4. Open the Python script of the model that you want to run (e.g., *runAWTY.py* for generating data needed for Figure 7(a) of the paper).
5. Set the *JMTPATH* variable (line 9) with the PATH of the JMT.jar file.
6. Save and exit.
7. Run the script using the command: *python runAWTY.py*.
8. When all simulations are completed, results are stored in a *CSV* file inside the *results/* directory.
9. Those data can be used to plot Figure 7(a). Please, open the *analysis_methodology.ipynb* jupyter notebook and run all cells in the *Are We There Yet?* section.
