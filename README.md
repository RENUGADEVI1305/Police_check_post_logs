# Police_check_post_logs

**Problem Statement:** Police check posts require a centralized system 
             for logging, tracking, and analyzing vehicle movements. 
             Currently, manual logging and inefficient databases slow down security processes. 

**AIM:**  The main aim of this project is to build an SQL-based check post database with a Python-powered dashboard for real-time insights and alerts.

**Skills:** Python, Pandas, MySQL, Data Analysis, Streamlit
| Tool               | Purpose                   |
|--------------------|---------------------------|
| **Python**         | Data handling & logic     |
| **Pandas**         | Data processing           |
| **MySQL / SQLite** | Backend data storage      |
| **Streamlit**      | UI for dashboard & queries|
| **Plotly**         | Interactive charts        |


** Installation Instructions **
Open my terminal in VS Code and run: pip install streamlit pandas mysql-connector-python matplotlib seaborn numpy plotly

1. **Data Collection**
   - Raw data from traffic stop records
   - Columns include: date, time, vehicle, gender, age, violation, outcome, etc.

2. **Data Storage (SQL)**
   - Data is cleaned and stored in a `cleaned_traffic_stops` table.

3. **Python & Pandas**
   - SQL queries executed using Python connector
   - Processed into clean DataFrames

4. **Streamlit**
   - Dashboard for metrics and filters
   - Interactive query execution
   - Vehicle lookup tool
   - Visual analytics (bar, pie, box charts)
  
  
