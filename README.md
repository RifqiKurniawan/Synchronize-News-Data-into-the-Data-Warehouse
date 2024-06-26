# Preface
**Disclaimer:** This is a form of documentation of a learning experience, possibly in the workplace. There are many ways to complete the process of data management challenges for different businesses depending on the problem.

# Overview
To create a robust and reliable ETL (Extract, Transform, Load) process for importing news data into a data warehouse. The source data is capable of hard delete operations, and the data extraction starts from the year 2016 using an incremental load approach.

**Languange Used**

Python - for creating data ingestion, incremental load and data orchestration 

SQL - for creating and querying the Postgres tables, data ingestion and ETL Process

Airflow - for data orchestration.

# Planning (Data Management Process)

The Data Management Process consist of:
* Data architecture - For General overview process
* Generate data - For generating news data that will be used
* Data Ingestion - For moving data from operational db to datawarehouse db
* Staging layer - For cleaning and pre-processing raw data on dwh
* Data warehouse layer - To Ensure that the data creation meets the user's requirements.
* Orchestration layer - for managing the execution of workflows via event-based triggers or time intervals

## Data Architecture

The main goal of creating this architecture is to understand the plan for building the ETL pipeline process from start to finish In accordance with the previously stated objective.
Here's data pipiline architecture that i used:

![](Images/ArchitectureETLProcess.JPG)

so this is step for the creation of this ETL process, 
  1. It starts with extracting news data already present in the PostgreSQL database using a Python process.
  2. The data will then be loaded into a data warehouse built using an Oracle database in the staging table.
  3. From the staging table, a transformation process will be carried out on the data in accordance with the points previously explained.

## Generate data
So, to create dummy data, I used a Python library called Faker. The data consists of 100,000 rows and includes several categories such as 'World', 'Technology', 'Sports', 'Business', 'Entertainment', 'Health', 'Politics', 'Technology', and 'Science'.

**Python Process**
![plot](Images/Generatedatapython.JPG)

**Excel Result**
![](Images/exceldatagenerate.JPG)

The next process, once the data has been generated, is to import it into the PostgreSQL database, where this table functions as an OLTP table. For detailed scripts, please refer to **Folder 1: Generate Data**(https://github.com/RifqiKurniawan/Synchronize_News_Data_into_the_DataWarehouse).

**Postgres Result**
![](Images/ResultPostgress1.JPG)


## Data Ingestion
Before performing the data ingestion process, we need to undertake several steps where we assume that the data we are bringing from the operational database is quite large (starting from 2016). Therefore, we need to perform an incremental load process, which involves fetching data in iterations to split the initial data retrieval process. This approach prevents overloading the environment of both the source and target databases.
**IncrementalLoad.py**

**Incrremental Load Process**
![plot](Images/IncrementalLoadDataPython.JPG)

**Result Load Process**
![plot](Images/IncrementalLoadDataOracle1.JPG)

## Staging layer
In this data Staging process, there are two processes to be created. 
The first process involves extracting data from the source by only taking delta data based on the created time and modified time. This approach ensures that the amount of data retrieved in each extraction is not excessive, thus avoiding overburdening the process (**Extract_News.py**). 

**Extract News**
![plot](Images/ExtractNews.JPG)

The second process involves extracting IDs from the source data for all records as a reference for comparison between the existing data in the data warehouse and the data in the source. This comparison enables the identification of data that has been hard deleted(**Extract_ID_News.py**).

**Extract ID News**
![plot](Images/ExtractID.JPG)

## Datawarehouse
In creating the ETL process for the data warehouse, there are two objectives for the results to be generated.(**ETL Process Oracle.sql**) 
Firstly, the main table adheres to the previous requirements, where it includes the creation date when the data is first entered into the data warehouse, the update date indicating the last time the data was updated, and the delete date, which is filled when the data is deleted. 

**Oracle Process DWH**
![plot](Images/ETLProcessOracle1.JPG)

Secondly, for the creation of SCD Type 4, it is utilized to store historical processes that can be used as a reference for CDC (Change Data Capture) if needed, with the note that only the latest changed data will be obtained.

**Versioning Table SCD Type 4**
![plot](Images/TableVersionSCD4.JPG)

## Orchestration layer ##

This brief guide covered the setup and usage of Apache Airflow with Python and Oracle connectors to orchestrate a data pipeline. The example workflow extracts news data using Python from postgres, processes it, and loads it into an Oracle database. By following these steps, you can create more complex workflows to handle various data engineering tasks.(**SYNC_PROCESS_1_HOUR.py**) 

![plot](Images/Airflow.JPG)


