# iSpot — A cost-effective transient server provisioning framework for predictable performance of big data analytics

iSpot is a lightweight and cost-effective instance provisioning framework for Directed Acyclic Graph (DAG)-style big data analytics, in order to guarantee the application performance on cloud transient servers (i.e., EC2 spot instances, GCE preemptible instances). 

## Architecture and Modules of iSpot
iSpot leverage the LSTM-based price prediction and the performance model of Spark with the critical data checkpointing, iSpot is able to translate the big data analytics job and its performance goals (e.g., the expected completion time) from cloud customers into an appropriate number of transient servers with the cost-effective instance type.

### LSTM-based Price Prediction


### Instance Checkpoint & Restore


### Spark Performance Model


### Performance Guarantee & Cost Minimization



