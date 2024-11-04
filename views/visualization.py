import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show_info(df):
    # Generate column information as a summary table
    list_dtypes = [df[col].dtype for col in df.columns]
    list_nunique = [df[col].nunique() for col in df.columns]
    list_null_values = [df[col].isnull().sum() for col in df.columns]

    column_info_df = pd.DataFrame({
        "Data Type": list_dtypes,
        "# Unique Values": list_nunique,
        "# Null Values": list_null_values
    }, index=df.columns)
    
    return column_info_df

def show():
    st.title('Visualization of the Healthcare Dataset')
    st.markdown("---")

    # Load data
    data_path = "data/healthcare_dataset.csv"
    df = pd.read_csv(data_path)

    # Display dataset overview
    st.write("### Medical Data")
    st.dataframe(df)

    # Show basic statistics
    st.write("### Descriptive Statistics")
    st.table(df.describe().T)

    # Display column information
    st.write("### Information of Each Column")
    column_info_df = show_info(df)
    st.table(column_info_df)

    # Sidebar Filters
    st.sidebar.header("Filter Options")
    gender_filter = st.sidebar.selectbox("Select Gender", ["All", "Male", "Female"])
    if gender_filter != "All":
        df = df[df["Gender"] == gender_filter]

    # Visualization Options
    st.write("### Choose Visualization Type")
    plot_type = st.selectbox("Select Plot Type", [
        "Age Distribution", "Billing Amount by Medical Condition", "Admission Type Count", "Test Results by Blood Type",
        "Billing Amount by Insurance Provider", "Gender Distribution", "Hospital Admissions by Year", "Medication Usage",
        "Average Billing by Age Group", "Admission Duration by Condition", "Doctor vs. Medical Condition", "Room Number Distribution"
    ])

    # Visualization Logic
    if plot_type == "Age Distribution":
        fig, ax = plt.subplots()
        sns.histplot(df['Age'], bins=10, kde=True, ax=ax)
        ax.set_title("Age Distribution")
        st.pyplot(fig)

    elif plot_type == "Billing Amount by Medical Condition":
        fig = px.box(df, x="Medical Condition", y="Billing Amount", color="Medical Condition", title="Billing Amount by Medical Condition")
        st.plotly_chart(fig)

    elif plot_type == "Admission Type Count":
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="Admission Type", palette="viridis")
        ax.set_title("Admission Type Count")
        st.pyplot(fig)

    elif plot_type == "Test Results by Blood Type":
        fig = px.histogram(df, x="Blood Type", color="Test Results", title="Test Results by Blood Type")
        st.plotly_chart(fig)

    elif plot_type == "Billing Amount by Insurance Provider":
        fig = px.bar(df, x="Insurance Provider", y="Billing Amount", color="Insurance Provider", title="Billing Amount by Insurance Provider")
        st.plotly_chart(fig)

    elif plot_type == "Gender Distribution":
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="Gender", palette="coolwarm")
        ax.set_title("Gender Distribution")
        st.pyplot(fig)

    elif plot_type == "Hospital Admissions by Year":
        df['Year of Admission'] = pd.to_datetime(df['Date of Admission']).dt.year
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="Year of Admission", palette="magma")
        ax.set_title("Hospital Admissions by Year")
        st.pyplot(fig)

    elif plot_type == "Medication Usage":
        fig = px.pie(df, names="Medication", title="Medication Usage Distribution")
        st.plotly_chart(fig)

    elif plot_type == "Average Billing by Age Group":
        df['Age Group'] = pd.cut(df['Age'], bins=[0, 20, 40, 60, 80, 100], labels=["0-20", "21-40", "41-60", "61-80", "81+"])
        avg_billing = df.groupby('Age Group')['Billing Amount'].mean().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=avg_billing, x="Age Group", y="Billing Amount", palette="Spectral")
        ax.set_title("Average Billing by Age Group")
        st.pyplot(fig)

    elif plot_type == "Admission Duration by Condition":
        df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
        df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
        df['Duration'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x="Medical Condition", y="Duration", palette="viridis")
        ax.set_title("Admission Duration by Medical Condition")
        st.pyplot(fig)

    elif plot_type == "Doctor vs. Medical Condition":
        fig, ax = plt.subplots()
        sns.countplot(data=df, y="Doctor", hue="Medical Condition", palette="cool")
        ax.set_title("Doctor vs. Medical Condition")
        st.pyplot(fig)

    elif plot_type == "Room Number Distribution":
        fig, ax = plt.subplots()
        sns.histplot(df['Room Number'], bins=10, kde=True, ax=ax)
        ax.set_title("Room Number Distribution")
        st.pyplot(fig)
