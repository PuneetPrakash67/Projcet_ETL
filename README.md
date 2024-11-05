# Projcet_ETL
 # Reddit ETL Pipeline with Sentiment Analysis

## Table of Contents
1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Technologies Used](#technologies-used)
4. [AWS Setup](#aws-setup)
5. [Project Structure](#project-structure)
6. [Installation](#installation)
7. [Running the ETL Process](#running-the-etl-process)
8. [Airflow Setup](#airflow-setup)
9. [Execution Logs](#execution-logs)
10. [Results](#results)
11. [Future Work](#future-work)
12. [References](#references)

## Project Overview
This project aims to develop an ETL pipeline that fetches posts from Reddit, performs sentiment analysis on the titles, and stores the results in an AWS S3 bucket. The project utilizes AWS services such as EC2 for deployment, Airflow for orchestration, and integrates deep learning models for sentiment classification.

## Problem Statement
In today’s digital landscape, understanding user sentiment on platforms like Reddit is essential for businesses and researchers. This project addresses the challenge of extracting insights from Reddit posts by automating the extraction, transformation, and loading (ETL) process.

## Technologies Used
- **AWS Services**: EC2, S3, IAM
- **Python Libraries**: 
  - `pandas` for data manipulation
  - `requests` for API calls
  - `boto3` for AWS SDK
  - `transformers` for sentiment analysis
  - `matplotlib` and `seaborn` for data visualization
  - `airflow` for workflow orchestration

## AWS Setup
### AWS Account
1. Create an AWS account if you don’t have one.
2. Set up an EC2 instance with a suitable instance type (e.g., `t3.medium`).
3. Create an S3 bucket to store the output CSV files and plots.

### IAM Role
1. Create an IAM role with permissions to access S3 and attach it to your EC2 instance.

## Project Structure
reddit_etl_project/ ├── reddit_etl.py # ETL logic for fetching and processing Reddit posts ├── reddit_dag.py # Airflow DAG definition ├── requirements.txt # Required Python packages └── README.md # Project documentation


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/reddit_etl_project.git
   cd reddit_etl_project

## Install required packages:
pip install -r requirements.txt

## Running the ETL Process
## To run the ETL process manually:
python reddit_etl.py


## Airflow Setup
## Install Apache Airflow following the official documentation.

## Set up the Airflow environment and start the web server:
airflow db init
airflow webserver --port 8080
airflow scheduler

Add the reddit_dag.py to the dags folder in your Airflow installation directory.

## Access the Airflow UI at http://localhost:8080 and trigger the reddit_etl_dag.

## Logs for the ETL process can be found in the Airflow web interface. Ensure to monitor these logs for any errors or status updates.


INFO - Fetching 100 posts from r/google...
INFO - Fetched 100 posts so far...
INFO - DataFrame shape: (100, 5)
INFO - ETL process completed. Posts and visualization saved to S3.


## Results
## The output includes a CSV file containing the fetched Reddit posts along with their sentiment analysis results. A bar plot visualizing the sentiment distribution is also generated and saved to S3.

## Future Work
Enhance sentiment analysis by experimenting with different models.
Expand the ETL pipeline to include more data sources and advanced analytics.
Improve error handling and logging mechanisms.
## References
Transformers Documentation: Transformers
Boto3 Documentation: Boto3
Airflow Documentation: Apache Airflow