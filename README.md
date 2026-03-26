# Sakila DVD Rental Data Analysis

## Overview
This project performs a comprehensive data analysis on the **Sakila database**, which contains operational data for a fictional DVD rental business. The analysis explores various key business areas, including inventory management, customer rental behaviors, payment trends, and store operations. The primary objective is to demonstrate data importing, cleaning, feature engineering, and visualization techniques using Python and pandas.

## Dataset
The dataset consists of 15 relational CSV files that emulate a real-world database schema:
- `actor.csv` & `film_actor.csv`: Actor details and their film appearances.
- `address.csv`, `city.csv`, `country.csv`: Location data for stores and customers.
- `category.csv` & `film_category.csv`: Movie genres and categories.
- `customer.csv`: Customer account details.
- `film.csv` & `language.csv`: Detailed film attributes (ratings, rental rates, languages).
- `inventory.csv`: Physical tracking of film copies across stores.
- `payment.csv`: Customer payment and transaction records.
- `rental.csv`: Detailed logs of when movies were rented and returned.
- `staff.csv` & `store.csv`: Employees and branch locations.

## Contents
- `proj.ipynb` & `study.ipynb`: Jupyter Notebooks containing the end-to-end data analysis pipeline.
- `*.csv`: The raw data files spanning the Sakila database tables.

## Analysis Pipeline
The analysis in the notebooks follows a structured workflow:
1. **Importing Data**: Loading all 15 CSV files into pandas DataFrames.
2. **Data Cleaning**: Handling missing values and converting text columns into proper `datetime` objects.
3. **Feature Engineering**: Creating new variables such as `payment_year_month` and `rental_duration_days` to unlock time-series insights.
4. **Data Merging**: Joining multiple tables (`payment`, `rental`, `customer`, `inventory`, `film`) to create a unified `master` dataset for comprehensive metric calculation.
5. **KPI Calculation**: Identifying critical business metrics:
   - Total Revenue & Total Rentals
   - Average Payment Amount
   - Overdue/Active Rentals count
   - Top Customers by Revenue
6. **Data Visualization**: Generating charts to uncover trends:
   - Monthly Revenue Trends
   - Rental distributions by Movie Rating (e.g., PG-13, R, NC-17)

## Prerequisites
To run this project, ensure you have the following installed:
- Python 3.7+
- Jupyter Notebook
- Pandas
- Matplotlib
- Seaborn

## Getting Started
1. Clone or download this repository/folder to your local machine.
2. Ensure all `csv` files are located in the same directory as the notebooks.
3. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
4. Open `proj.ipynb` or `study.ipynb` and run the cells sequentially to reproduce the analysis.

## Key Insights
- The merged master dataset provides a unified view of the customer journey, from specific movie selection to transaction finalization.
- Revenue trends help identify the most profitable periods for the rental store.
- By tracking top-spending customers, business owners can design targeted loyalty and marketing campaigns.
