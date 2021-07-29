import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px

st.set_page_config(layout="wide")
@st.cache
def load_data():
    df = pd.read_csv('data/data.csv',encoding='cp1252', low_memory=False)

    cols_to_rmv = ['stn_code','sampling_date', 'spm', 'pm2_5', 'agency','location_monitoring_station']
    df.drop(cols_to_rmv, axis=1, inplace=True)
    df['type'] = df['type'].fillna('Others')
    df['location'].fillna(df.location.mode()[0], inplace=True)
    df['date'].fillna(df.date.mode()[0], inplace=True)

    df['type'].replace('Residential, Rural and other Areas','Residential',inplace = True)
    df['type'].replace('Residential and others','Residential',inplace = True)
    df['type'].replace('Industrial Areas','Industrial',inplace = True)
    df['type'].replace('Industrial Area','Industrial',inplace = True)
    df['type'].replace('Sensitive Area','Sensitive',inplace = True)
    df['type'].replace('Sensitive Areas','Sensitive',inplace = True)
    df['type'].replace('RIRUO','Rural',inplace = True)

    df.replace(to_replace= 'Visakhapatnam', value = 'Vishakhapatnam', inplace = True)
    df.replace(to_replace= 'Silcher', value = 'Silchar', inplace = True)
    df.replace(to_replace= 'Kotttayam' , value = 'Kottayam', inplace = True)
    df.replace(to_replace= 'Bhubaneswar' , value = 'Bhubaneshwar', inplace = True)
    df.replace(to_replace= 'Pondichery' , value = 'Pondicherry', inplace = True)
    df.replace(to_replace= 'Noida, Ghaziabad' , value = 'Noida', inplace = True)
    df.replace(to_replace= 'Calcutta', value = 'Kolkata', inplace = True)
    df.replace(to_replace= 'Greater Mumbai', value = 'Mumbai', inplace = True)
    df.replace(to_replace= 'Navi Mumbai', value = 'Mumbai', inplace = True)
    df.replace(to_replace= 'Bombay', value = 'Mumbai', inplace = True)
    df.replace(to_replace= 'andaman-and-nicobar-islands', value = 'Andaman & Nicobar Islands', inplace = True)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df.drop('date', axis = 1, inplace=True)

    return df

limit = 100
df = load_data()

so2_state_groupby = df.groupby('state')['so2'].mean()
no2_state_groupby = df.groupby('state')['no2'].mean()
rspm_state_groupby = df.groupby('state')['rspm'].mean()

df1 = pd.DataFrame(so2_state_groupby)
df2 = pd.DataFrame(no2_state_groupby)
df3 = pd.DataFrame(rspm_state_groupby)
state_df = df1.merge(df2, left_index= True, right_index= True).merge(df3, left_index= True, right_index= True)
sloc = state_df
sloc['index'] = sloc.index.tolist()
st.write(sloc)

wmap = folium.Map(location=[25,80], zoom_start=4)
wmap.choropleth(
    geo_data='data/india_states.json',
    name='choropleth',
    data=sloc,
    columns=['index', 'so2'],
    key_on='feature.properties.NAME_1',
    fill_color='YlOrRd',
    fill_opacity=0.75,
    line_opacity=0.3,
    legend_name='SO2 Distribution Across India'
)
folium_static(wmap)
