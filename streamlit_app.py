import streamlit as st
import requests

API_URL = "http://localhost:8000/api/todo/"

st.title("ToDo App")

title = st.text_input("Title")
description = st.text_area("Description")

if st.button("Create ToDo"):
    response = requests.post(API_URL, json={"title": title, "description": description})
    if response.status_code == 200:
        st.success("ToDo item created successfully!")
    else:
        st.error("Failed to create ToDo item.")
