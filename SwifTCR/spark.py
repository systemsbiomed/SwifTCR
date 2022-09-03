__all__ = ['spark_cluster']


# Clusters a list of strings using spark. session.
def spark_cluster(string_list, return_rdd=False, output_path='./cluters.csv'):
    try:
        import findspark
        findspark.init()
        
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName('SwifTCR').getOrCreate()

    except (ImportError, ValueError):
        raise('Someting went wrong with the Spark cluster.')
    else:
        string_list = list(filter(lambda s: isinstance(s, str) and len(s)>=2, string_list))
        # Converts a list of seq_lists to an RDD.
        seq_list_rdd = spark.sparkContext.parallelize(string_list)
        # Converts a list of RDDs to a flat list of substings.
        substings_rdd = seq_list_rdd.flatMap(lambda s: [((s[:skip]+s[skip+1:], skip), s) for skip in range(len(s))])
        

        
        # Convert a cluster to a CSV line
        csv_line = cluster_rdd.map(lambda c: (c[0][1],','.join(c[1])))
        
        # Convert CDR3s to CSV format
        cluster_df = csv_line.toDF(["edit_index", "CDR3s"])
        
        # write csv to output_path
        cluster_df.write.csv(output_path)
        


# Cluster sequences by key.
def cluster_sequences(sequence_rdd):
                
        # Convert a string to a set.
        def to_set(a):
            return {a}

        # A decorator to add a and b.
        def add(a, b):
            a.add(b)
            return a

        # Updates a and b.
        def update(a, b):
            a.update(b)
            return a
        
        # Creates a new RDD containing all substings of the cluster.
        cluster_rdd = sequence_rdd.combineByKey(to_set, add, update).filter(lambda c: len(c[1])!=1)


# Creates a spark clustering RDD from a substing key.
def spark_cluster_rdd(substing_key_rdd):
    grouped_rdd = substing_key_rdd.reduceByKey(lambda a,b: a+b)
    cluster_rdd = grouped_rdd.values()
    cluster_rdd2 = cluster_rdd.filter(lambda x: len(x)>1)
    return cluster_rdd2

