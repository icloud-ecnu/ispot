# iSpot — A cost-effective transient server provisioning framework for predictable performance of big data analytics

iSpot is a lightweight and cost-effective instance provisioning framework for Directed Acyclic Graph (DAG)-style big data analytics, in order to guarantee the application performance on cloud transient servers (i.e., EC2 spot instances, GCE preemptible instances) while minimizing the budget cost. 

## Overview of iSpot
Leveraging the LSTM-based price prediction and the performance model of Spark with the critical data checkpointing, iSpot is able to translate the big data analytics job and its performance goals (e.g., the expected completion time) from cloud customers into an appropriate number of transient servers with the cost-effective instance type. The overview of iSpot is illustrated in the following figure.
<div align=center><img width="550" height="300" src="https://github.com/icloud-ecnu/ispot/blob/master/images/architecture.png"/></div>

## LSTM-based Price Prediction
We train the LSTM model with a subset of price data, which is divided into n<sub>steps</sub>. Within each step, the input price with n<sub>input</sub> sequential price data is mapped onto the hidden layer with a dimension of d. In more detail, the i-th input price, i.e., a n<sub>input</sub> &times;1 vector ip<sub>i</sub> = <p<sub>1</sub>,p<sub>2</sub>,...,p<sub>n<sub>input</sub></sub>>, is transformed to a n<sub>input</sub> &times; d matrix hl<sub>i</sub>. Each hidden layer affects its following layers, and the price variation is captured by accumulating such effects along the n<sub>steps</sub> sequential hidden layers. The output price opn<sub>steps</sub> can be calculated as n<sub>input</sub> &times; 1 vector based on the last hidden layer and the last input price. The former process is sampled and repeated for n<sub>batch</sub> &times; 1 in order to accelerate the model computation.

## Spark Performance Model
The model of a Spark job is built based on the lineage graph of RDDs, which is illustrated by the DAG information of stages in the following figure.
<div align=center><img width="400" height="200" src="https://github.com/icloud-ecnu/ispot/blob/master/images/DAG.png"/></div>
<br>Such DAG information illustrates the dependency of consecutive stages. Given the stage set of a job S = {S<sub>1</sub>,S<sub>2</sub>,...,S<sub>n</sub>}, the completion time of a Spark job T<sub>job</sub> can be considered as the completion time of the last stage block, which is given by 
<div align=center><img width="400" height=30" src="https://github.com/icloud-ecnu/ispot/blob/master/images/Tjob.png"/></div>
As the stages are executed in parallel and blocked by the ancestor stages, the completion time of a stage block i is calculated by adding the stage execution time to the maximal block time of its ancestor stages. In particular, the upper bound and the lower bound of T<sub>job</sub> can be given by 
<div align=center><img width="300" height=40" src="https://github.com/icloud-ecnu/ispot/blob/master/images/Boundary.png"/></div>
We proceed to model the execution time of each stage i as below,
<div align=center><img width="300" height=30" src="https://github.com/icloud-ecnu/ispot/blob/master/images/Tstage.png"/></div>
where T<sup>i</sup><sub>sh</sub>,T<sup>i</sup><sub>pr</sub>,and T<sup>i</sup><sub>gc</sub> denote the data shuffling, data processing and data (de)serialization and garbage collectiontime of the stage i, respectively.
<br>In particular, our analytical performance model for Spark can be extended to the other dataflow processing frameworks(e.g., Dryad, TensorFlow), which is left as our future work.</br>
  
## Instance Checkpoint & Restore
To mitigate the RDD recovery overhead caused by the instance revocations, we integrate
our critical data checkpointing mechanism elaborated into Spark v2.0.1 by modifying the source codes of Spark. In more detail, we checkpoint the critical RDDs using rdd.persist() to remote disks in the cluster (modified in DAGScheduler.scala). The files which we have modified are listed in the directory of Spark-checkpointing. You can download and replace them in the source code and then build Spark using Maven. Example:

```
# Apache Hadoop 2.7.X and later
./build/mvn -Pyarn -Phadoop-2.7 -Dhadoop.version=2.7.3 -DskipTests clean package
```
If downloading dependencies from the maven repository is too slow, you can use Alibaba Cloud's repository or build a nexus local private repository.

## Performance Guarantee & Cost Minimization
After using provisioning algorithm to get the number and type of instance, we leverage automatic scripts to request new instances in the stable availability zones and to deploy the Spark cluster. The shell scripts in directory Cluster help to reduce many manual configuration steps.


