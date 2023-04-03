# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime, timedelta

import openai
import streamlit as st


openai.api_key = st.secrets["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"]


example_destinations = ['Paris', 'London', 'New York', 'Tokyo', 'Sydney', 'Hong Kong', 'Singapore', 'Warsaw', 'Mexico City', 'Palermo']
random_destination = random.choice(example_destinations)

now_date = datetime.now()

# round to nearest 15 minutes
now_date = now_date.replace(minute=now_date.minute // 15 * 15, second=0, microsecond=0)

# split into date and time objects
now_time = now_date.time()
now_date = now_date.date() + timedelta(days=1)

def generate_prompt(destination, arrival_date, departure_date,departure_time,arrival_time,**kwargs):
    return f'''
*Think like 20 years experience trip advisor and prepare the trip schedule for the {destination} most rated famous place considering arrival time as {arrival_time} and  and departure time as {departure_time} strictly and Use the example format: always keep day in next row, cover as many places as possible,keep the same format for output:
*Arrival Date: {arrival_date}
*Departure Date: {departure_date}


Example:
[Day]: Morning– Start the day with Dolphin Sight Seeing Tour from Panaji jetty, Visit Dona Paula Jetty , Miramar beach & Shopping Malls of Panaji city. 
Afternoon: Lunch break at [give 3 Close by good rating economical hotel names for lunch near to last place in morning schedule] near Miramar beach or Dona Paula Jetty Area 
Evening: Spend time exploring Old Goa Churches like Se Cathedral, Basilica of Bom Jesus. take a dinner at [give 3 close by good rating economical hotels for dinner near to last visit place in the evening] near Basilica of bom Jesus. 
'''.strip()


def submit():    
    prompt = generate_prompt(**st.session_state)
    print(prompt)
    # generate output
    output = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0.45,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=0,
        max_tokens=1024
    )
    
    st.session_state['output'] = output['choices'][0]['text']
    #response = output['choices'][0]['text']
    #print(response)
    
# Initialization
if 'output' not in st.session_state:
    st.session_state['output'] = '--'

st.title('Trip Scheduler')
st.subheader('Let us plan your trip!')


with st.form(key='trip_form'):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader('Destination')
        origin = st.text_input('Destination', value=random_destination, key='destination')
        st.form_submit_button('Submit', on_click=submit)

    with c2:
        st.subheader('Arrival')
        st.date_input('Arrival Date', value=now_date, key='arrival_date')
        st.time_input('Arrival Time', value=now_time, key='arrival_time')

    with c3:
        st.subheader('Departure')
        st.date_input('Departure Date', value=now_date + timedelta(days=1), key='departure_date')
        st.time_input('Departure Time', value=now_time, key='departure_time')

    
st.subheader('Trip Schedule')
st.write(st.session_state.output)
