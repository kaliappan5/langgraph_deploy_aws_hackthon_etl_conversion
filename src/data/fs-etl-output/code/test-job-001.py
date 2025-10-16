Here's the equivalent PySpark code using the DataFrame API based on the provided ETL steps:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Customer ETL") \
    .getOrCreate()

# Step 1: Extract Customers
df_customers = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://your_mysql_host:3306/your_database") \
    .option("dbtable", "customers") \
    .option("user", "your_username") \
    .option("password", "your_password") \
    .load()

# Step 2: Filter Active
df_active_customers = df_customers.filter(col("status") == "active")

# Step 3: Load to S3
df_active_customers.write \
    .mode("overwrite") \
    .format("parquet") \
    .save("s3://fs-data-output/customers_active")

# Stop the Spark session
spark.stop()
```

This PySpark code does the following:

1. Initializes a Spark session.

2. Extracts data from the MySQL "customers" table. Note that you'll need to replace `your_mysql_host`, `your_database`, `your_username`, and `your_password` with your actual MySQL connection details.

3. Applies a filter to keep only active customers.

4. Writes the resulting DataFrame to S3 in Parquet format.

5. Stops the Spark session.

Remember to have the necessary dependencies in your Spark environment:
- MySQL JDBC driver (for connecting to MySQL)
- AWS SDK for Java (for writing to S3)

You might need to configure Hadoop AWS settings in your Spark configuration to enable S3 access, depending on your Spark setup.