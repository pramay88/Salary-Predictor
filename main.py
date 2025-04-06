import streamlit as st
from prediction import predict_salary,get_salary_stats
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



df = pd.read_csv("Dataset.csv")



global input_experience, input_job_roles,input_region,predicted_salary

job_roles = ["Software Engineer", "Full Stack Developer", "Data Scientist", "Machine Learning Engineer", "Cybersecurity Analyst", "DevOps Engineer", "Cloud Engineer", "UI/UX Designer", "Blockchain Developer", "IoT Developer", "Game Developer", "Embedded Systems Engineer"]
regions = ["India", "USA"]

# UI
st.set_page_config(page_title="Salary Predictor", page_icon="💰", layout="centered")
   
st.markdown("<h1 style='text-align: center;'>💰 Salary Predictor</h1>", unsafe_allow_html=True)

st.divider()
with st.form("myform", clear_on_submit=False, border=True):
    # st.write("Enter Job Role: ")

    input_job_roles = st.selectbox("Enter Job Role:", job_roles,index=None,placeholder="Choose a job role" )
    # st.write(" ")
    input_experience = st.number_input('Enter your experience (in years):')

    input_region = st.selectbox("Enter region:", regions,index=None,placeholder="Choose a region" )
    submitbtn = st.form_submit_button("Submit") 
if submitbtn:
    if not (input_job_roles==None or input_experience == None ):
        
        st.success("Form Submitted Successfully")
        # progress_bar = st.progress(0, text=None)
        # for i in range(100):
        #     time.sleep(0.001)
        #     progress_bar.progress(i + 1)
        # time.sleep(1)
        # progress_bar.empty()

        st.divider()
        # global predicted_salary
        predicted_salary = predict_salary(job_role=input_job_roles, years_of_experience=input_experience)
        
        st.markdown("<h2 style='text-align: center;'>Prediction Report</h2>", unsafe_allow_html=True)

        st.subheader(f"Job Role: {input_job_roles}")
        st.subheader(f"Experience: {input_experience} Years")
        st.success(f"Predicted Salary: {predicted_salary:,.2f}")

        

        st.divider()

        # Detailed Analysis
        st.markdown("<h2 style='text-align: center;'>Detailed Analysis</h2>", unsafe_allow_html=True)
        
        st.header("1. Basic Stats")
        col1, col2, col3 = st.columns(3)
        min, avg, max = get_salary_stats(input_job_roles)
        col1.metric(label="Minimun", value=f"{min:,.2f}", delta="₹", border=True, delta_color="off")
        col2.metric(label="Average", value=f"{avg:,.2f}", delta="₹", border=True, delta_color="off")
        col3.metric(label="Maximun", value=f"{max:,.2f}", delta="₹", border=True, delta_color="off")

        st.divider()

        st.header("2. Salary vs Experience:")

        # ExperienceVSsalary plot
        filtered_df = df[df["Job_Role"] == input_job_roles].sort_values("Years_of_Experience")        
        st.line_chart(filtered_df.set_index("Years_of_Experience")["Average_Salary"], x_label="Experience (in years)", y_label="Salary in ₹")
        
        

        st.divider()

        # Average Salary by Job Role
        st.subheader("💼 Average Salary by Job Role")
        job_salary_df = df.groupby("Job_Role")["Average_Salary"].mean().reset_index()
        st.bar_chart(job_salary_df.set_index("Job_Role"))


        st.divider()

        # Salary Trend Over Experience for Different Roles
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df, x="Years_of_Experience", y="Average_Salary", hue="Job_Role", ax=ax)
        ax.set_title("Salary Growth Over Experience (All Roles)")
        st.pyplot(fig)

        st.divider()

        # Pie Chart
        st.subheader("📊 Salary Distribution by Job Role")

        fig, ax = plt.subplots()
        ax.pie(job_salary_df["Average_Salary"], labels=job_salary_df["Job_Role"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular

        st.pyplot(fig)

        st.divider()

        # 🔥 Top 5 Highest-Paying Roles  
        st.subheader("🔥 Top 5 Highest-Paying Roles")  
        top_jobs = df.groupby("Job_Role")["Average_Salary"].mean().sort_values(ascending=False).head(5)  
        st.bar_chart(top_jobs)

        st.divider()

        # if show_analysis_btn==True:
        #     show_analysis()


    else:
        st.error("Please fill the Details")

