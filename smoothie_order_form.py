# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"🥤Customize Your Smoothie!🥤")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

# Get the current credentials
cnx=st.connection("snowflake")
session=cnx.session()
#session = get_active_session()

# option=st.selectbox(
#     'What is your preferred fruit?',
#     ('Apple','Banana','Strawberry'),
#     index=None,
#     placeholder='Select a fruit'
# )

# st.write('You selected: ',option)


name=st.text_input("Enter you name",value="")
if name:
    st.write("Your name is: ",name)


my_dataframe=session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe,use_container_width=True)

ingredients_list=st.multiselect('Select upto 5 ingredients',
                                my_dataframe,
                                max_selections=5,
                                placeholder='Select your ingredients')

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string=''
    for x in ingredients_list:
        ingredients_string+=x+' '

    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name + """')"""

    st.write(my_insert_stmt)

    time_to_insert=st.button("SUBMIT ORDER")
    
    if time_to_insert:
        result=session.sql(my_insert_stmt)
        st.write(result)
        
    # if len(ingredients_string)==5:
    #     result=session.sql(my_insert_stmt)
    #     st.write(result)

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
