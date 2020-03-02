# SF Crime Statistics with Spark Streaming

## Overview 

Given a real-world dataset, extracted from Kaggle, on San Francisco crime incidents, provides statistical analyses of the data using Apache Spark Structured Streaming. also creates a Kafka server to produce data, and ingest data through Spark Structured Streaming. 

## Requirements

* Java 1.8.x
* Scala 2.11.x
* Spark 2.4.x
* Kafka
* Python 3.6 or above

## Environment Setup
This project requires creating topics, starting Zookeeper and Kafka servers, and your Kafka bootstrap server. You’ll need to choose a port number (e.g., 9092, 9093..) for your Kafka topic, and come up with a Kafka topic name and modify the zookeeper.properties and server.properties appropriately.

Install requirements using `./start.sh` if you use conda for Python. If you use pip rather than conda, then use `pip install -r requirements.txt`

## Instructions

In order to run the application you will need to start:

### Step 0. Start the Zookeeper and Kafka Server:
```
`bin/zookeeper-server-start.sh config/zookeeper.properties`
`bin/kafka-server-start.sh config/server.properties`
```
### Step 1. Produce data into topic by kafka Producer:
`python kafka_server.py`

### Step 1.1. Run Kafka consumer to test if Kafka Producer is correctly implemented and producing data:

Option 1: `kafka-console-consumer --topic "topic-name" --from-beginning --bootstrap-server localhost:9092`
Option 2: `python consumer_server.py`

### Step 2. Submit Spark Streaming Job :

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py`

## Example of Kafka Consumer and Spark Streaming output
### Kafka Consumer Console Output

![kafka consumer output](https://github.com/taihangFu/SF-Crime-Statistics-with-Spark-Streaming/blob/master/screenshot/Kafka%20Consumer%20Console%20Output.png)

### Progress Reporter

![progress reporter](https://github.com/taihangFu/SF-Crime-Statistics-with-Spark-Streaming/blob/master/screenshot/Screen%20Shot%202020-02-25%20at%205.46.06%20pm.png)


### Spark UI
![spark UI](https://github.com/taihangFu/SF-Crime-Statistics-with-Spark-Streaming/blob/master/screenshot/Screen%20Shot%202020-02-25%20at%205.46.43%20pm.png)


## Question 1

> How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

It changes `processedRowsPerSecond`


## Question 2
> What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

To increase the throughput, the most efficient way is to update the #message read/second and #partitions, which are 
`spark.streaming.kafka.maxRatePerPartition` and `spark.sql.shuffle.partitions` repectively.

From my experiements, tuning `spark.streaming.kafka.maxRatePerPartition` seems no effect on the `processedRowsPerSecond`. 

However, tuning `spark.sql.shuffle.partitions` is obviously affacting the value of `processedRowsPerSecond`.
The default `spark.sql.shuffle.partitions` is 200, which is too large for a 2 core machine where I submit my spark program on. 
I run experiments range of numbers from 2-100 and I found the optimal is when `spark.sql.shuffle.partitions` = 2 which lead to the highest possible throughput I could possibly achived: `processedRowsPerSecond` = 300+.


```
spark.sql.shuffle.partitions = 2                
spark.streaming.kafka.maxRatePerPartition = 200  
```
