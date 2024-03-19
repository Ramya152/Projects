import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

#URL of the file hosted on Backblaze B2
file_url = "https://f005.backblazeb2.com/file/HomicideReport1520/Homicide+Report.csv"
file_path = "/Users/ramyaamudapakula/Downloads/HomicideReport.csv"

#Downloading the file using requests library
response = requests.get(file_url)

#Checking if the request was successful
if response.status_code == 200:
    # Writing the content of the response to the file
    with open(file_path, "wb") as file:
        file.write(response.content)
    print("File downloaded successfully.")
else:
    print("Failed to download file. Status code:", response.status_code)

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

data = load_data()

#Filtering the dataset for relevant columns
agency_data = data[['Agency Type', 'Crime Solved']]

#Grouping the data by agency name and count the number of solved and unsolved cases
agency_counts = agency_data.groupby(['Agency Type', 'Crime Solved']).size().unstack(fill_value=0)

#Creating a  Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Visualization", "View Data"))

st.title("Homicides Report, 1980-2014 Data Analysis")

if page == "Visualization":
    st.header("Number of Solved and Unsolved Cases by Law Enforcement Agencies")
    fig, ax = plt.subplots(figsize=(10, 6))
    agency_counts.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Number of Solved and Unsolved Cases by Law Enforcement Agencies")
    ax.set_xlabel("Law Enforcement Agency")
    ax.set_ylabel("Number of Cases")
    ax.set_xticklabels(agency_counts.index, rotation=45, ha='right')
    st.pyplot(fig)
elif page == "View Data":
    st.header("View Subset of Data")
    st.dataframe(data.head(10))
