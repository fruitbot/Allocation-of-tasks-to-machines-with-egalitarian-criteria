# Assigning-tasks-to-machines-in-data-centers

The goal of this project is to implement algorithms to assign tasks (representing processes) to machines in data centers. 

Each task i has a size pi and a type ti (a type can represent for example a web server, a database, a calculation which uses the processor intensively, etc.). For each pair of types (t1, t2), there exists a compatibility coefficient α(t1, t2) which indicates to what extent tasks of types t1 and t2 can be placed on the same machine without interfering. 

We will allocate n tasks to m machines. Given the assignment of tasks to the machines, the cost of a task i placed on the machine M (i) is ci = Σ pj * α(tj, ti) (the higher the cost, the less the performance the task is good). The cost of the system is the maximum cost of a task (it measures the quality of service offered to the tasks).

The problem we will consider is to assign the tasks to the machines so as to minimize the cost of the system.





## Brief descriptions 
_Note: Project's report contains complete information._



### Algorithms

* **LPT** Largest-processing-time-first sequencing. A sequencing rule in scheduling theory that prioritizes jobs (or tasks) to be scheduled according to an order of their non-increasing processing times.

* **Juxtaposed**  By employing other scheduling algorithms, this one aims to find the best partition of machines to allocate a list of tasks of two types.

* **Greedy Cluster**  analyses the compatibility of different tasks, and cluster the tasks which are interfered the least when they are put on the same machine. 

* **PTAS**  Polynomial time approximation scheme, which tries to schedule the tasks in the most optimal way whose time complexity is polynomial instead of exponential.



### Others

* **tkinter** tkinter is used in this project to generate the graphical interface which shows the allocation clearly and efficiently.

* **Matplotlib** By controling the amount of tasks and machines or the coefficient of compatibility, it compares the validity, efficiency and complexity of different algorithms.





## Contributors

Félicité LORDON, Shuting ZHANG and David SARMIENTO


