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
