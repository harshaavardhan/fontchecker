# app_streamlit.py
import streamlit as st
import requests
from bs4 import BeautifulSoup

def clean_font(font_family):
    return font_family.replace('"', '').replace("'", "").strip()

def get_font_families(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Couldn't fetch the website: {str(e)}"}, 400
    
    soup = BeautifulSoup(response.text, 'html.parser')
    styles = soup.find_all('style')
    
    font_families = []
    
    for style in styles:
        style_content = style.string if style.string else style.get_text()
        if style_content:
            font_families += parse_font_families(style_content)
    
    if not font_families:
        return {"error": "No font families found on the website"}, 404
    
    return list(set(font_families))

def parse_font_families(style_content):
    found_fonts = []
    lines = style_content.split(';')
    for line in lines:
        if 'font-family' in line:
            line = line.strip()
            font_family_value = line.split('font-family:')[-1].strip()
            found_fonts.extend([clean_font(font) for font in font_family_value.split(",")])
    
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
            for font in result:
                st.write(font)
    else:
        st.write("Please enter a valid URL.")
