# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 18:49:13 2020

@author: Felipe
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.title('The PhDs job market')

@st.cache
def load_salaries_data():
    
    file = 'data/sed17-sr-tab049.xlsx'
    data = pd.read_excel(file, skiprows=3)
    data.columns = ['field','academia','industry','government','nonprofit','other']
    return data

data_load_state = st.text('Loading data...')
salaries = load_salaries_data()



data_load_state.text("Done! (using st.cache)")

#Scatterplot

st.subheader('It (almost) always pays to leave the Academia')

option = st.selectbox(
    'Which employer would you like to compare with academia?',
    ('industry', 'government', 'nonprofit','other')
    )
st.write('You selected:', option)

selected_data = salaries.loc[:,['field','academia',option]]
selected_data['pispo'] = round(100 * salaries['academia']/salaries[option], 0)
selected_data = selected_data.sort_values('pispo', ascending=False)

salary_scatterplot = px.scatter(selected_data , 
                                x = 'academia',
                                y = option,
                                size='pispo',
                                color='pispo',
                                hover_name = 'field',
#                                range_x=[40000,140000],
#                                range_y=[40000,140000],
                                labels = {'industry':'PhD salary in industry',
                                          'academia':'PhD salary in academia',
                                          'government':'PhD salary in government',
                                          'nonprofit':'PhD salary in non-profit organizations',
                                          'other':'PhD salary in other types of organizations',
                                          'pispo':'Percent of ' + option + ' salary paid by academia'},
                                title = 'Does an academic carreer pay off?'
                                )

st.plotly_chart(salary_scatterplot, use_container_width=True)

if st.checkbox('Show ranking'):
    st.subheader('Ranking')
    selected_data = selected_data.rename(columns={'pispo': 'Percent of ' + option + ' salary paid by academia'})
    st.write(selected_data)


@st.cache
def load_unemployment_data():
    
    file = 'data/sed17-sr-tab042.xlsx'
    data = pd.read_excel(file, skiprows=3)
    data= data.iloc[19:,:]
    data = pd.melt(data, id_vars='Commitment status and year')
    data.columns = ['year','field','unemployed']
    return data

data_load_state = st.text('Loading data...')
unemployed= load_unemployment_data()
data_load_state.text("Done! (using st.cache)")

st.subheader('1 in every 3 PhDs graduate with no job or post-doc in view')

if st.checkbox('Filter specialization'):
    chosen_field = st.selectbox('Choose the field of specialization:',sorted(list(set(unemployed.field))))
    unemployed = unemployed[unemployed.field == chosen_field]


unemployed_trends = px.line(unemployed,
       x = 'year',
       y = 'unemployed',
       color = 'field',
       range_y=[0,50],
       title='% of PhDs graduating with no employment nor post-doc commitment',
       labels={'year': 'Year', 'unemployed': '% of PhDs graduating with no employment or post-doc'})

st.plotly_chart(unemployed_trends, use_container_width=True)

