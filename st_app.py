import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
import plotly.express as px




def create_connection():
    mydb =mysql.connector.connect(
        host = "localhost",
        user = "root",
        password="",
        database="DS_project_1",
        autocommit = True)
    
    mycursor=mydb.cursor(buffered=True)
    return mydb 

st.set_page_config(page_title="Police Check Data")

st.sidebar.title("My Dashboard")
page=st.sidebar.radio('Visit',["Home", "Project Explanation", "Police Check Data Analysis", "SQL Queries", "Predict Outcome and Violation Log", "Developer Info"])


   # page1 -  Home 

if page == "Home":
    
    st.header("Home")
    st.markdown(" ## Mini project 1:  ")
    st.markdown(" ### Title - Secure Check: A Python-SQL Digital Ledger for Police Post Logs")
    st.image("D:/GUVI/project1/images/pic1.jpg")

  # page2 -  Project Explanation 

elif page == "Project Explanation":
    st.header("Project Explanation")
    st.image("D:/GUVI/project1/images/pic2.jpg", width=300)
    st.write(""" **Problem Statement:** Police check posts require a centralized system 
             for logging, tracking, and analyzing vehicle movements. 
             Currently, manual logging and inefficient databases slow down security processes.  """)
    
    st.write(" **AIM:**  The main aim of this project is to build an SQL-based check post database with a Python-powered dashboard for real-time insights and alerts.")
    
    st.subheader("Dataset")
    df=pd.read_csv("D:/GUVI/project1/cleaned_traffic_stops.csv") 
    st.dataframe(df)

   # page3 -  Police Check Data Analysis 

elif page == "Police Check Data Analysis":
    st.header("Police Check Data Analysis")

    st.subheader("🔎 Filters")
          
    df=pd.read_csv("D:/GUVI/project1/cleaned_traffic_stops.csv") 
    vehicle_input = st.text_input("🔍 Enter vehicle number:")

    if vehicle_input:
        matching_vehicles = df[df['vehicle_number'].str.contains(vehicle_input, case=False)]

        if not matching_vehicles.empty:
           selected_vehicle = st.selectbox("Select vehicle number from matches:", matching_vehicles['vehicle_number'].unique())
           vehicle_data = df[df['vehicle_number'] == selected_vehicle]

           st.subheader("📊 Vehicle Stop Metrics")

           col1, col2, col3, col4 = st.columns(4)

           with col1:
             st.metric("Total Stops", value=len(vehicle_data))

           with col2:
            st.metric("Arrests", value=vehicle_data['is_arrested'].sum())

           with col3:
            st.metric("Drug-Related Stops", value=vehicle_data['drugs_related_stop'].sum())

           with col4:
            st.metric("Unique Violations", value=vehicle_data['violation'].nunique())

           with st.expander("🔎 View Stop Details"):
            st.dataframe(vehicle_data.reset_index(drop=True))

        else:
                 st.warning("No matching vehicle numbers found.")
    else:
      st.info("Please enter a vehicle number to begin search.")

    
    selected_country = st.selectbox("Select Country", ["All"] + sorted(df['country_name'].dropna().unique().tolist()))
     
    df['stop_date'] = pd.to_datetime(df['stop_date'], format="%d-%m-%Y")
    start_date = df['stop_date'].min().date()
    end_date = df['stop_date'].max().date()

    date_range = st.date_input("Select Date Range", [start_date, end_date])

    filtered_df = df.copy()
    if selected_country != "All":
       filtered_df = filtered_df[filtered_df['country_name'] == selected_country]

       if date_range:
          filtered_df = filtered_df[
          (filtered_df['stop_date'] >= pd.to_datetime(date_range[0])) &
          (filtered_df['stop_date'] <= pd.to_datetime(date_range[1]))
           ]

          # 1. Interactive Bar Chart: Top 10 stopped vehicles
          st.subheader("🚗 Top 10 Stopped Vehicles")
          top_vehicles = filtered_df['vehicle_number'].value_counts().head(10).reset_index()
          top_vehicles.columns = ['vehicle_number', 'stop_count']
          fig_bar = px.bar(top_vehicles, x='vehicle_number', y='stop_count', title='Top 10 Most Stopped Vehicles')
          st.plotly_chart(fig_bar)

          # 2. Interactive Pie Chart: Arrests
          st.subheader("🚨 Arrest Distribution")
          arrest_counts = filtered_df['is_arrested'].value_counts().rename({0: "Not Arrested", 1: "Arrested"}).reset_index()
          arrest_counts.columns = ['Arrest Status', 'Count']
          fig_pie = px.pie(arrest_counts, names='Arrest Status', values='Count', title='Arrest Distribution')
          st.plotly_chart(fig_pie)


    
    tab1, tab2,tab3,tab4= st.tabs(["driver_race","violation","stop_outcome","driver_gender"])

    
    with tab1:
     if not df.empty and 'driver_race' in df.columns:
          driver_race_df=df['driver_race'].value_counts().reset_index()
          driver_race_df.columns=['driver_race','count']
          fig=px.pie(driver_race_df,names='driver_race',values='count', title='driver_race',color='driver_race')
          st.plotly_chart(fig,use_container_width=True)
     else:
          st.warning("No data available")
    with tab2:
     if not df.empty and 'violation' in df.columns:
          violation_df=df['violation'].value_counts().reset_index()
          violation_df.columns=['violation','count']
          fig=px.bar(violation_df,x='violation',y='count', title='stops by violation',color='violation')
          st.plotly_chart(fig,use_container_width=True)
     else:
          st.warning("No data available")
    with tab3:
     if not df.empty and 'stop_outcome' in df.columns:
          stop_outcome_df=df['stop_outcome'].value_counts().reset_index()
          stop_outcome_df.columns=['stop_outcome','count']
          fig=px.bar(stop_outcome_df,x='stop_outcome',y='count', title='stops by stop_outcome',color='stop_outcome')
          st.plotly_chart(fig,use_container_width=True)
     else:
          st.warning("No data available")
    with tab4:
     if not df.empty and 'driver_gender' in df.columns:
          driver_gender_df=df['driver_gender'].value_counts().reset_index()
          driver_gender_df.columns=['driver_gender','count']
          fig=px.pie(driver_gender_df,names='driver_gender',values='count', title='driver_gender',color='driver_gender')
          st.plotly_chart(fig,use_container_width=True)
     else:
          st.warning("No data available")


    if 'country_name' in df.columns and 'driver_age' in df.columns:
       fig = px.box(
        df,
        x='country_name',
        y='driver_age',
        title='Distribution of Driver Age by Country',
        color='country_name',
        points='all'  # shows all individual data points
        )
       st.plotly_chart(fig, use_container_width=True)
    else:
     st.warning("Required columns not found in dataset.")





 
  # page4 -  SQL Queries 
 
elif page == "SQL Queries":
    st.header("SQL Queries")
    st.subheader("Medium level:")
    queries={
       "1. Total Number of Police Stops": "SELECT count(*) AS No_of_Police_stops FROM police_check_data",
       "2. Count of Stops by Violation Type": "SELECT Violation, COUNT(*) AS Violation_stops FROM police_check_data GROUP BY Violation ORDER BY Violation_stops DESC",
       "3. Number of Arrests vs. Warnings ":"SELECT stop_outcome,COUNT(*) AS Count FROM police_check_data WHERE stop_outcome IN ('Arrest', 'Warning') GROUP BY stop_outcome ORDER BY count DESC ",
       "4. Average Age of Drivers Stopped ":"SELECT AVG(driver_age) AS Avg_driver_age  FROM police_check_data ",
       "5. Top 5 Most Frequent Search Types ":"SELECT  search_type, COUNT(*) AS count   FROM police_check_data GROUP BY search_type ORDER BY count DESC LIMIT 5 ",
       "6. Count of Stops by Gender ":"SELECT  driver_gender AS gender, COUNT(*) AS stop_count   FROM police_check_data GROUP BY driver_gender ",
       "7. Most Common Violation for Arrests ":"SELECT  Violation, COUNT(*) AS arrest_count   FROM police_check_data WHERE is_arrested=TRUE GROUP BY Violation  ORDER BY arrest_count DESC LIMIT 1 ",
       "8. Average Stop Duration for Each Violation ":"""SELECT  Violation, AVG( CASE 
                                                        WHEN stop_duration = '0-15 Min' THEN 7.5
                                                        WHEN stop_duration = '16-30 Min' THEN 23
                                                        WHEN stop_duration = '30+ Min' THEN 35
                                                        ELSE NULL
                                                        END) AS avg_stop_duration   FROM police_check_data GROUP BY Violation""",
       "9. Number of Drug-Related Stops by Year ":"SELECT  YEAR(stop_date) AS stop_year, COUNT(*) AS drugs_related_stop_counts  FROM police_check_data WHERE drugs_related_stop=TRUE GROUP BY stop_year  ORDER BY stop_year ",
       "10. Drivers with the Highest Number of Stops ":"SELECT  vehicle_number, COUNT(*) AS drivers_stops  FROM police_check_data GROUP BY vehicle_number  ORDER BY drivers_stops DESC LIMIT 5 ",
       "11. Number of Stops Conducted at Night (Between 10 PM - 5 AM) ":"SELECT   COUNT(*) AS stops_at_night  FROM police_check_data WHERE TIME(stop_time)>= '22:00:00' OR TIME(stop_time) <= '05:00:00' ",
       "12. Number of Searches Conducted by Violation Type ":"SELECT violation,  COUNT(*) AS count_of_searches  FROM police_check_data WHERE search_conducted=TRUE GROUP BY violation ORDER BY count_of_searches DESC ",
       "13. Arrest Rate by Driver Gender ":"SELECT driver_gender,  ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate  FROM police_check_data  GROUP BY driver_gender ",
       "14. Violation Trends Over Time (Monthly Count of Violations) ":"SELECT violation,  MONTH(stop_date) AS month,  COUNT(*)  AS counts  FROM police_check_data  GROUP BY MONTH(stop_date), violation ORDER BY counts DESC ",
       "15. Most Common Stop Outcomes for Drug-Related Stops":"SELECT stop_outcome,  COUNT(*)  AS counts  FROM police_check_data WHERE drugs_related_stop=TRUE GROUP BY stop_outcome ORDER BY counts DESC ", 
    }

    selected_query_list = st.selectbox("Choose a query", list(queries.keys()))
    selected_query=queries[selected_query_list]

    if st.button("Run Query",  key="run_query_button_1"):
        conn=create_connection()
        mycursor=conn.cursor(buffered=True)

        
        mycursor.execute(selected_query)
        data=mycursor.fetchall()
        columns=[i[0] for i in mycursor.description]

        query_result=pd.DataFrame(data,columns=columns)

        st.write("### Query Result:")
        st.dataframe(query_result)

        mycursor.close()
        conn.close()


    st.subheader("Complex level:")
    queries={
     "1. Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)":"""SELECT year, country_name, total_stops, arrest_count 
                 FROM (SELECT country_name,YEAR(stop_date) AS year, 
                 COUNT(*) OVER (PARTITION BY YEAR(stop_date), country_name) AS total_stops, 
                 SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)
                  OVER (PARTITION BY YEAR(stop_date), country_name) AS arrest_count 
                  FROM police_check_data) AS sub
                  GROUP BY year, country_name, total_stops, arrest_count
                 ORDER BY year, country_name """,
     "2. Driver Violation Trends Based on Age and Race (Join with Subquery)":"SELECT violation, sub.age, sub.race,   COUNT(*)  AS counts  FROM (SELECT  violation, driver_age AS age, driver_race AS race FROM police_check_data ) AS sub  GROUP BY violation,  sub.age, sub.race ORDER BY counts DESC",
     "3. Time Period Analysis of Stops (Joining with Date Functions)":"""SELECT YEAR(STR_TO_DATE(stop_date, '%Y-%m-%d')) AS year, 
                 MONTH(STR_TO_DATE(stop_date, '%Y-%m-%d')) AS month,
                 DAYNAME(STR_TO_DATE(stop_date, '%Y-%m-%d')) AS weekday, 
                 HOUR(STR_TO_DATE(stop_time, '%H:%i')) AS hour, COUNT(*)  AS stop_counts  FROM police_check_data 
                 GROUP BY  year, month, weekday, hour ORDER BY year, month, weekday, hour""",
     " 4. Correlation Between Age, Violation, and Stop Duration (Subquery)":"""SELECT 
                 violation, 
                 driver_age_group,
                 ROUND(AVG(stop_duration_minutes), 2) AS avg_stop_duration,                  
                 COUNT(*)  AS counts 
                FROM 
                 (SELECT CASE WHEN driver_age < 18 THEN '<18'
                WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
                WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                ELSE '60+'
                END AS driver_age_group,
                violation,
                CASE stop_duration
                WHEN '0-15 Min' THEN 10
                WHEN '16-30 Min' THEN 23
                WHEN '30+ Min' THEN 35
                ELSE NULL
                END AS stop_duration_minutes  FROM police_check_data) AS sub
                GROUP BY violation, driver_age_group ORDER BY counts DESC  """,
     "5. Violations with High Search and Arrest Rates (Window Function)":"""SELECT violation, search_type, ROUND(AVG(search_conducted)*100, 2) AS search_rate, 
                 ROUND(AVG(is_arrested)*100, 2) AS arrest_rate, RANK() OVER (ORDER BY AVG(search_conducted) DESC) AS search_rank,
                 RANK() OVER (ORDER BY AVG(is_arrested) DESC) AS arrest_rank,  COUNT(*)  AS counts  FROM police_check_data GROUP BY violation, search_type ORDER BY search_rank""",
     "6. Driver Demographics by Country (Age, Gender, and Race)":"""SELECT country_name,  driver_gender, ROUND(AVG(driver_age), 1) AS avg_age,
                 driver_race, COUNT(*)  AS counts  FROM police_check_data  GROUP BY country_name, driver_gender, driver_race ORDER BY country_name, counts DESC""",
     "7.Top 5 Violations with Highest Arrest Rates": """SELECT violation, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate,
                 COUNT(*)  AS police_stops  FROM police_check_data  GROUP BY violation ORDER BY arrest_rate DESC LIMIT 5""",
       }

    selected_query_list = st.selectbox("Choose a query", list(queries.keys()))
    selected_query=queries[selected_query_list]

    if st.button("Run Query", key="run_query_button_2"):
        conn=create_connection()
        mycursor=conn.cursor(buffered=True)

        
        mycursor.execute(selected_query)
        data=mycursor.fetchall()
        columns=[i[0] for i in mycursor.description]

        query_result=pd.DataFrame(data,columns=columns)

        st.write("### Query Result:")
        st.dataframe(query_result)

        mycursor.close()
        conn.close()


 
     # page5 -  Predict Outcome and Violation Log
elif page == "Predict Outcome and Violation Log":
  st.header("Predict Outcome and Violation Log")
    
  with st.form("new_post_log_form"):
   
    stop_date=st.date_input('Stop date', value=datetime.date.today())
    stop_time = st.time_input("Select a time", value=datetime.time(9, 0), step=datetime.timedelta(minutes=1))
    country_name=st.selectbox("Country name",['Canada', 'India', 'USA'])
    driver_gender=st.selectbox("Driver gender",['Male', 'Female'])
    driver_age=st.number_input("Driver age", min_value=18, max_value=80, step=1)
    driver_race=st.selectbox("Driver race",['Asian', 'Other', 'Black', 'White', 'Hispanic'])
    violation=st.selectbox("Violation",['Speeding', 'Other', 'DUI', 'Seatbelt', 'Signal'])
    search_type=st.selectbox("Search type",['Vehicle Search', 'Frisk'])
    search_conducted=st.selectbox("Was a search conducted",['1', '0'])
    stop_outcome=st.selectbox("Stop outcome",['Ticket', 'Arrest', 'Warning'])
    drugs_related_stop=st.selectbox("Was a drugs related",['1', '0'])
    stop_duration=st.selectbox("Stop duration",['16-30 Min', '0-15 Min', '30+ Min'])
    vehicle_number=st.text_input("Vehicle number")

  
    timestamp=pd.Timestamp.now()

    submitted=st.form_submit_button("Predict stop outcome and violation")
    df = pd.read_csv("D:/GUVI/project1/cleaned_traffic_stops.csv")


    if submitted:
        filtered_data = df[
            (df['driver_gender'] == driver_gender) &
            (df['driver_age'] == driver_age) &
            (df['search_conducted'] == int(search_conducted)) &
            (df['stop_duration'] == stop_duration) &
            (df['drugs_related_stop'] == int(drugs_related_stop)) 
        ]
        if not filtered_data.empty:
            predicted_outcome=filtered_data['stop_outcome'].mode()[0]
            predicted_violation=filtered_data['violation'].mode()[0]
        else:
            predicted_outcome="warning"
            predicted_violation="speeding"

        search_text="A search was conducted" if int(search_conducted) else "No search was conducted"
        drug_text="was drug_related" if int(drugs_related_stop) else "was not drug-related"

        st.markdown(f""" 
                 🧠 Prediction summary 
                    
                🔍predicted stop outcome: {predicted_outcome}
                🚨predicted violation: {predicted_violation}
        
         👤 A {driver_age}-year-old {driver_gender} driver in {country_name} was 
         stopped at {stop_time.strftime('%I:%M %p')} on {stop_date}.
         🔎 {search_text}, and 💊 the stop {drug_text}.
        
        ⏱️ stop duration: {stop_duration}.
         🚗 vehicle number: {vehicle_number}.

        """)

   # page6 -  Developer Info
 
elif page == "Developer Info":
    st.header("Developer Info")
    st.markdown("""
    **Developed by:** T RENUGADEVI 

    **Course:** Data Science                        
    **Skills:** Python, Pandas, MySQL, Data Analysis, Streamlit""", True)

    st.snow()
