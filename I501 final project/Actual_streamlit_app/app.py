import os
from utils.b2 import B2
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 


# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
REMOTE_DATA = 'Homicide Report.csv'


# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'],
        secret_key=os.environ['B2_APPKEY'])


# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
@st.cache_data
def get_data():
    # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df_homicide = b2.get_df(REMOTE_DATA)
    
    # Filtering the dataset for relevant columns
    agency_data = df_homicide[['Agency Type', 'Crime Solved']]

    # Grouping the data by agency name and count the number of solved and unsolved cases
    agency_counts = agency_data.groupby(['Agency Type', 'Crime Solved']).size().unstack(fill_value=0)
    
    return df_homicide, agency_counts

# Call the get_data() function to retrieve df_homicide and agency_counts
df_homicide, agency_counts = get_data()

# Creating a Sidebar
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
    st.dataframe(df_homicide.head(10))
