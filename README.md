# CommunityDetection-Spark-AWS

A Spark application, written in Python3, to figure out [**strongly connected components**][strongly connected components] with Bi-directional Label Propagation algorithm.

This project implemented an 1.3GB Twitter network dataset by AWS EMR cluster. 

[strongly connected components]:https://en.wikipedia.org/wiki/Strongly_connected_component

## How to replicate the experiment
   - Upload labelp.py and dataset to your bucket in AWS S3. (if you already have an [**AWS account**][AWS account])
   
   - Create a cluster in AWS EMR. </br>
   
     - Launch mode : `Step execution` (You can also choose `Cluster` and use `SSH` to connect your cluster.) </br>
     
     - Step type : `Spark application` </br>
       (configure) </br> 
       Name : `labelp` </br> 
       Deploy mode : `cluster` </br>
       Spark-submit options : `-- master yarn --driver-memory 4g --executor-memory 2g` . Without setting memory, application may fail for memoryoverhead. (For more details : [**Running Spark on Yarn**][Running Spark on Yarn])</br>
       Application location : `choose labelp.py in your S3 bucket` </br>
       Action on failure : `Terminate cluster` (Recommended) </br>
    
     - Vendor : `Amazon`, Release : `emr-5.2.0` (If you choose `Cluster` mode before, choose Application : `Spark: Spark 2.0.2...`.) </br>
     
     - Instance type : `m1.large` </br>
       Number of instances : `4` </br>
       (You can use other type and number of instances, but make sure that your total memory is larger than 13.91G, which was observed as the maximum memory used during the process.) </br>
       (The whole time for computation was about 6 hour and 43 mins.)
       
     - Permission : `Default` </br>
       (If you choose `Cluster` mode before, upload your public key to AWS and select it here) </br>
       
     - Click `Create cluster` button. </br>
       Done! </br>
       Your cluster will be terminated automatically after the application is finished.
 
[AWS account]:https://aws.amazon.com/
[Running Spark on Yarn]:http://spark.apache.org/docs/latest/running-on-yarn.html

## Where to find the dataset I used

[**Dataset : Twitter**][Dataset : Twitter] </br>
R. Zafarani and H. Liu, (2009). Social Computing Data Repository at ASU [http://socialcomputing.asu.edu]. Tempe, AZ: Arizona State University, School of Computing, Informatics and Decision Systems Engineering

[Dataset : Twitter]:http://socialcomputing.asu.edu/datasets/Twitter

## Results
Output format : `('Label',u'CommunitySize/Members')` </br>
See [**output-refined version**][output-refined version].

[output-refined version]:https://github.com/linghaol/CommunityDetection-Spark-AWS/tree/master/output-refined%20version

## Details of Algorithm
Please read [**Algorithm Instruction.pdf**][Algorithm Instruction.pdf].

[Algorithm Instruction.pdf]:https://github.com/linghaol/CommunityDetection-Spark-AWS/blob/master/Algorithm%20Instruction.pdf

## Want a Pseudo distributed version to test small datasets?
Please see [**pseudo mode**][pseudo mode].

[pseudo mode]:https://github.com/linghaol/CommunityDetection-Spark-AWS/tree/master/pseudo%20mode
  
## Dataset in other format?
With a dataset using (space) or (tab) to separate follower and user, </br>
change the following position: </br>
  - (line 11 & 51) `y=x.split(',') --> y=x.split()`
  
## Others
If you have any question or suggestion, please contact llh455398472@gmail.com or linghaol@usc.edu . </br>
Thanks! </br>

Linghao Li </br>
12/19/2016

