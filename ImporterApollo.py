import streamlit as st
import requests

# Streamlit app title
st.title('Apollo API Search Interface')

# Sidebar for API parameters
st.sidebar.header('API Parameters')

# Using st.secrets for securely handling the API key
api_key = st.secrets["api_key"]
# Other parameters for the API request
domains = st.sidebar.text_area('Organization Domains (separate by newline)', 'apollo.io\ngoogle.com')
page = st.sidebar.number_input('Page', min_value=1, value=1)
per_page = st.sidebar.number_input('Results per Page', min_value=1, max_value=100, value=10)
locations = st.sidebar.text_area('Locations (separate by newline)', 'California, US')
seniorities = st.sidebar.multiselect('Seniorities', ['senior', 'manager'], default=['senior', 'manager'])
employees_ranges = st.sidebar.text_input('Number of Employees Range', '1,1000000')
titles = st.sidebar.text_area('Person Titles (separate by newline)', 'sales manager\nengineer manager')

# Button to make the request
if st.button('Search'):
    # Preparing the data for the POST request
    data = {
        "api_key": api_key,
        "q_organization_domains": domains.split('\n'),
        "page": page,
        "per_page": per_page,
        "organization_locations": locations.split('\n'),
        "person_seniorities": seniorities,
        "organization_num_employees_ranges": [employees_ranges],
        "person_titles": titles.split('\n')
    }

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }

    # Making the POST request
    url = "https://api.apollo.io/v1/mixed_people/search"
    response = requests.post(url, headers=headers, json=data)

    # Checking if the request was successful
    if response.status_code == 200:
        # Displaying the response
        st.success('API Request Successful!')
        st.json(response.json())
    else:
        # Displaying an error message
        st.error(f'API Request Failed: {response.status_code}')
