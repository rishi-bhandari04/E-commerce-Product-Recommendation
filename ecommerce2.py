import streamlit as st
import pandas as pd
from main import get_recommendations_with_details
from sklearn.preprocessing import LabelEncoder

# GENERAL SETTINGS
PAGE_TITLE = "Ecommerce Demo"
PAGE_ICON = ":wave:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# Session State Initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['users'] = {'admin': 'password'}  # Default user for testing

def load_data():
    data = pd.read_csv('amazon.csv')
    return data

@st.cache_data  # Caching for faster reloading
def get_data():
    return load_data()

def display_selected_product_details(selected_product_details):
    """
    Display the product details of the selected product
    """
    st.header("Selected Product Details")
    st.write(f"Product ID: {selected_product_details['product_id']}")
    st.write(f"Product Name: {selected_product_details['product_name']}")
    st.write(f"Category: {selected_product_details['category']}")
    st.write(f"Rating: {selected_product_details['rating']} ({selected_product_details['rating_count']})")

def display_selected_product_image(selected_product_details):
    st.image(selected_product_details['img_link'], use_column_width=True)
    st.write(f"Product Link: [Link]({selected_product_details['product_link']})")

def display_recommendations(recommendations):
    """
    Display recommendations when product id is received
    """
    st.header(f"Recommendations")
    num_columns = 2  # Number of columns in the grid layout
    num_recommendations = len(recommendations)
    num_rows = (num_recommendations - 1) // num_columns + 1

    columns = st.columns(num_columns)

    recommendation_index = 0
    for row in range(num_rows):
        for col in range(num_columns):
            if recommendation_index >= num_recommendations:
                break

            with columns[col]:
                recommendation = recommendations[recommendation_index]
                st.subheader(f"Recommendation {recommendation_index + 1}")
                st.write(f"Product ID: {recommendation['product_id']}")
                st.write(f"Product Name: {recommendation['product_name']}")
                st.write(f"Category: {recommendation['category']}")
                st.write(f"Rating: {recommendation['rating']} ({recommendation['rating_count']})")
                st.image(recommendation['img_link'], use_column_width=False)
                st.write(f"Product Link: [Link]({recommendation['product_link']})")
                recommendation_index += 1

def registration_page():
    st.title('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Register'):
        if username in st.session_state['users']:
            st.error('Username already exists')
        else:
            st.session_state['users'][username] = password
            st.success('User registered successfully!')

def login_page():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username in st.session_state['users'] and st.session_state['users'][username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success('Logged in successfully!')
        else:
            st.error('Invalid username or password')

def main():
    """
    Main function where you can select the category and a product.
    By which you can get the recommendations
    """
    st.title('Ecommerce Demo')

    # Load the dataset
    data = get_data()

    st.title('Filter Category')
    # Filter products by category
    selected_category = st.selectbox('Select a category:', sorted(data['category'].unique()))
    filtered_data = data[data['category'] == selected_category]

    st.title("Product Recommendations")

    # Create an input field for the user to enter the product ID
    product_id_encoder = LabelEncoder()
    selected_product_name = st.selectbox('Select a product:', sorted(filtered_data['product_name'].values))

    # Check if a product is selected
    if selected_product_name:
        # Get the product ID for the selected product name
        selected_product_id = filtered_data[filtered_data['product_name'] == selected_product_name]['product_id'].values[0]
        product_id_encoder.fit(data['product_id'])
        product_id = product_id_encoder.transform([selected_product_id])[0]

        selected_product_details = filtered_data[filtered_data['product_id'] == selected_product_id].iloc[0]
        details_col, image_col = st.columns(2)
        # Display product details in the left column
        with details_col:
            display_selected_product_details(selected_product_details)

        # Display product image and link in the right column
        with image_col:
            display_selected_product_image(selected_product_details)

    # Button to trigger the recommendations
    if st.button("Get Recommendations"):
        # Call the recommendation function with default parameter values
        recommendations = get_recommendations_with_details(product_id=product_id)
        display_recommendations(recommendations)

# Check if user is logged in
if not st.session_state['logged_in']:
    login_page()
    st.write("Don't have an account?")
    if st.button("Register"):
        registration_page()
else:
    main()
