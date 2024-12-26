# -*- coding: utf-8 -*-
"""population_growth_app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gBFb-geZjq1eRGxdbkHG01-aetJ5YK4n
"""

!pip install streamlit

import streamlit as st

# Title
st.title("Population Growth Analysis")

# Input Fields
st.header("Input Parameters")
number_of_births = st.number_input("Number of Births", min_value=0, step=1, value=1000)
possible_deaths = st.number_input("Number of Deaths", min_value=0, step=1, value=500)
immigrants = st.number_input("Number of Immigrants", min_value=0, step=1, value=300)
emigrants = st.number_input("Number of Emigrants", min_value=0, step=1, value=100)
total_population = st.number_input("Total Population", min_value=1, step=1, value=10000)

# Calculate Growth Rate
growth_rate = (((number_of_births - possible_deaths) + (immigrants - emigrants)) / total_population) * 100

# Display Growth Rate
st.subheader("Population Growth Rate")
st.write(f"The calculated growth rate is **{growth_rate:.2f}%**")

# Insights
st.subheader("Insights")
if growth_rate > 0:
    st.success("The population is increasing. This can positively contribute to development and investment opportunities.")
else:
    st.warning("The population is decreasing. This might indicate potential challenges in growth and sustainability.")