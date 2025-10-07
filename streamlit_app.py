# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The Name on your smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    for ing in ingredients_list:
        ingredients_string += ing + ' '
        st.subheader(ing + ' Nutrition Infromation')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + ing)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    button = st.button("Submit Order")

    if button:
        session.sql(my_insert_stmt).collect()
        output_string = "Your Smoothie is ordered, " + name_on_order + "!"
        st.success(output_string, icon="✅")
