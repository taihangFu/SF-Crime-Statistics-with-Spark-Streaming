# SF Crime Project

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
