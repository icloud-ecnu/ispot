# iSpot — A cost-effective transient server provisioning framework for predictable performance of big data analytics

iSpot is a lightweight and cost-effective instance provisioning framework for Directed Acyclic Graph (DAG)-style big data analytics, in order to guarantee the application performance on cloud transient servers (i.e., EC2 spot instances, GCE preemptible instances). 

## Architecture and Modules of iSpot
iSpot leverages the LSTM-based price prediction and the performance model of Spark with the critical data checkpointing, iSpot is able to translate the big data analytics job and its performance goals (e.g., the expected completion time) from cloud customers into an appropriate number of transient servers with the cost-effective instance type.

![](https://github.com/icloud-ecnu/ispot/blob/master/images/architecture.png) 

## LSTM-based Price Prediction
We train the LSTM model with a subset of price data, which is divided into n<sub>steps</sub>. Within each step, the input price with n<sub>input</sub> sequential price data is mapped onto the hidden layer with a dimension of d. In more detail, the i-th input price, i.e., a n<sub>input</sub> * 1 vector ip<sub>i</sub> = <p<sub>1</sub>,p<sub>2</sub>,...,p<sub>n<sub>input</sub></sub>>, is transformed to a n<sub>input</sub> * d matrix hl<sub>i</sub>. Each hidden layer affects its following layers, and the price variation is captured by accumulating such effects along the n<sub>steps</sub> sequential hidden layers. The output price opn<sub>steps</sub> can be calculated as n<sub>input</sub> * 1 vector based on the last hidden layer and the last input price. The former process is sampled and repeated for n<sub>batch</sub> * 1 in order to accelerate the model computation.

## Spark Performance Model

## Instance Checkpoint & Restore
To mitigate the RDD recovery overhead caused by the instance revocations, we integrate
our critical data checkpointing mechanism elaborated into Spark v2.0.1 by modifying the source codes of Spark. In more detail, we checkpoint the critical RDDs using rdd.persist() to remote disks in the cluster (modified in DAGScheduler.scala). The files which we have modified was list in the directory of Spark-checkpointing, you can download and replace in the source code, then build Spark using Maven. Example:

```
# Apache Hadoop 2.7.X and later
./build/mvn -Pyarn -Phadoop-2.7 -Dhadoop.version=2.7.3 -DskipTests clean package
```
If you think that downloading dependencies from the maven repository is too slow, you can use Alibaba Cloud's repository or build a nexus local private repository.

## Performance Guarantee & Cost Minimization
After using provisioning algorithm get the number and type of instance, we using some automatic scripts to request new instance in the stable availability zones and deploy the Spark cluster. The shell scripts in directory Cluster help you to reduce many manual configuration steps.


