
import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd


# from auth0.authentication import GetToken
# from auth0.authentication import Users


# def authenticate(username, password):
#     domain = 'dev-xjwfdu0f3ch27icm.us.auth0.com'
#     client_id = 'lATAkSYzAKcVJ8oOBCNj4bmAEPOKjr4M'
#     client_secret = 'Pkqms7Uv4SYQDmBuJScAL8U69QPmcMLHub6tsxSEmQFmMhedXvmPukC3gnMMN33i'
#     get_token = GetToken(domain)
    
#     token = get_token.client_credentials(client_id, client_secret, 'https://YOUR_AUTH0_DOMAIN/api/v2/')


#     token = get_token.login(client_id=client_id, client_secret=client_secret,
#                             username=username, password=password,
#                             realm='Username-Password-Authentication',
#                             scope='openid')
#     user_info = Users(domain).userinfo(token['access_token'])
#     return user_info

# username = st.text_input("Enter username:")
# password = st.text_input("Enter password:", type="password")


# if st.button("Login"):
#     user = authenticate(username, password)
#     if user:
# st.success("Logged in successfully")

option = st.selectbox('Choose an Option:', ('Option 1', 'Option 2', 'Option 3'), key='unique_key_0')

value = st.slider('Choose a value:', min_value=0, max_value=100, key='unique_key_1')

value = st.slider('Choose a value:', min_value=0, max_value=100, key='unique_key_2')

if st.button('API Call 1'):
    pass

if st.button('API Call 2'):
    pass

if st.button('API Call 3'):
    pass

if option == 'Option 1':
    data = pd.DataFrame({'x': range(10), 'y': range(10)}) # Sample data
    plt.plot(data['x'], data['y'])
    st.pyplot(plt)
# Add conditions for other options



    # else:
    #     st.warning("Incorrect username or password")

