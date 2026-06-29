# Aura Health & Wellness - OmniChannel Marketing Data Pipeline

## Project Overview
This is a personal data engineering project I built to solve a realistic business problem for a mock company called Aura Health & Wellness. 

**The Problem:** Aura's customer profiles were stuck in a CRM database (CSV format), while their website traffic logs were sitting in a separate web clickstream folder (JSON format). Because the data was siloed, the marketing team couldn't track how much a customer's website behavior matched their actual spending habits.

**The Solution:** I built an end-to-end cloud data pipeline using a **Medallion Lakehouse Architecture** (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) on Azure to ingest both datasets, clean them up, and combine them into a final analytics table for marketing insights.

---

## How the Pipeline Works

1. **Data Mocking:** I wrote a local Python script using the `Faker` library to generate realistic CRM customer profiles and nested website clickstream logs.
2. **Bronze Layer (Ingestion):** Uploaded the raw CSV and JSON files directly into Azure Data Lake Storage Gen2 (ADLS).
3. **Silver Layer (Cleaning):** Used Azure Databricks and PySpark to clean the data. I dropped missing customer IDs, removed duplicate website sessions, and fixed data types (like turning string timestamps into real dates). The clean data was saved back to Azure as Delta tables.
4. **Gold Layer (Analytics):** Mapped the Silver tables to temporary SQL views in Databricks. I wrote SQL queries to calculate Customer Lifetime Value (CLV) and group users into marketing segments.

---

## Math & Marketing Logic Used

### 1. Customer Lifetime Value (CLV) Formula
To predict how much a customer is worth to the company over a year based on how often they visit the site, I used this formula in my SQL query:

$$CLV = Total\_Historical\_Spend \times \left( \frac{Frequency}{Datediff(Current\_Date, Signup\_Date)} \times 365 \right)$$

### 2. Marketing Segmentation (SQL Case When)
I wrote conditional rules to automatically tag customers based on their value and recency (how many days since their last visit):
* **VIP Champions:** Spent over \$1,000 in total AND visited the site in the last 30 days. (Perfect for loyalty rewards).
* **At-Risk Churn:** Spent over \$200 but haven't visited the site in over 120 days. (Needs a win-back email).
* **Standard Active:** Everyone else who is browsing normally.

---

## Tech Stack
* **Cloud Storage:** Azure Data Lake Storage Gen2 (ADLS)
* **Compute / Notebooks:** Azure Databricks (Spark)
* **Storage Format:** Delta Lake 
* **Languages:** Python (PySpark) & SQL
