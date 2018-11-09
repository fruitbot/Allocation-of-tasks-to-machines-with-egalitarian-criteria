# Assigning-tasks-to-machines-in-data-centers

The goal of this project is to implement algorithms to assign tasks (representing processes) to machines in data centers. 

Each task i has a size pi and a type ti (a type can represent for example a web server, a database, a calculation which uses the processor intensively, etc.). For each pair of types (t1, t2), there exists a compatibility coefficient α(t1, t2) which indicates to what extent tasks of types t1 and t2 can be placed on the same machine without interfering. 

We will allocate n tasks to m machines. Given the assignment of tasks to the machines, the cost of a task i placed on the machine M (i) is ci = Σ pj * α(tj, ti) (the higher the cost, the less the performance the task is good). The cost of the system is the maximum cost of a task (it measures the quality of service offered to the tasks).

The problem we will consider is to assign the tasks to the machines so as to minimize the cost of the system.



## Brief descriptions of algorithms

* **LPT** Hat tip to anyone whose code was used
* etc

## Contributors

Félicité LORDON, Shuting ZHANG and David SARMIENTO
