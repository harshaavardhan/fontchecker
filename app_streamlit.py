# app_streamlit.py
import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_font_families(url):
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Couldn't fetch the website"}, 400
    
    soup = BeautifulSoup(response.text, 'html.parser')
    styles = soup.find_all('style')
    
    font_families = []
    
    for style in styles:
        style_content = style.string
        if style_content:
            font_families += parse_font_families(style_content)
    
    return list(set(font_families))

def parse_font_families(style_content):
    found_fonts = []
    lines = style_content.split(';')
    for line in lines:
        if 'font-family' in line:
            line = line.strip()
            font_family_value = line.split('font-family:')[-1].strip()
            found_fonts.append(font_family_value)
    
    return found_fonts

st.title("Fetch Font Families from Website")
url = st.text_input("Enter the URL of the website:")

if st.button("Fetch"):
    if url:
        result = get_font_families(url)
        if "error" in result:
            st.write(result["error"])
        else:
            st.write("Font Families found:")
            st.write(result)
    else:
        st.write("Please enter a valid URL.")
