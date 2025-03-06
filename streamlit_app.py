# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    f"""Replace the code in this example app with your own code! And if you're new to Streamlit.

    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be: ' , name_on_order)

#session = get_active_session()
cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME') , col('SEARCH_ON'))
#st.dataframe(data = my_dataframe , use_container_width = True)
#st.stop()

#convert spark dataframe into pandas dataframe so we can use LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients : ' 
                                  , my_dataframe
                                  , max_selections = 5)

if ingredients_list:

    ingredients_string = ''
    
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen , 'SEARCH_ON'].iloc[0]
        st.write(The search value for ' , fruit_choosen , ' is ' , search_on , '.')
                 
        st.subheader(fruit_choosen + ' Nutrition Information')

        #st.text(ingredients_string)

        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
        #st.text(smoothiefroot_response.json())
        st_df = st.dataframe(data = smoothiefroot_response.json() , use_container_width = True)

    my_insert_stmt = """ Insert into SMOOTHIES.PUBLIC.ORDERS(  name_on_order , ingredients)
            values (' """ + name_on_order + """ ' , ' """ + ingredients_string + """ ') """

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:

        session.sql(my_insert_stmt).collect()

        st.success('Your Smothie is ordered ,' + name_on_order + '!'  , icon="✅")
