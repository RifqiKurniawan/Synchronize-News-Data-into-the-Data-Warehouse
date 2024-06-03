# Preface
**Disclaimer:** This is a form of documentation of a learning experience, possibly in the workplace. There are many ways to complete the process of data management challenges for different businesses depending on the problem.

# Overview
To create a robust and reliable ETL (Extract, Transform, Load) process for importing news data into a data warehouse. The source data is capable of hard delete operations, and the data extraction starts from the year 2016 using an incremental load approach.

**Key Components:**
Source Data Characteristics:

The source data contains news articles.
       The data source supports hard delete operations, meaning records can be permanently removed.
Data Extraction Start Point:
      Data extraction begins from the year 2016.
Incremental Load Process:
      The ETL process is designed to handle incremental loads to efficiently manage and update the data warehouse.

Here's why I used each language:

Python - for creating the pipelines connecting the different layers

SQL - for creating and querying the Postgres tables

Although cloud data warehouses are growing increasingly popular in the analytics world, there are still scenarios where traditional data warehouses would serve an enterprise better than a cloud data warehouse. More on this will be shared in a future blog post.
