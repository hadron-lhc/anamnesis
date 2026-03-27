import streamlit as st
from custom import apply_custom_styles


# Definir páginas
pages = [
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/search.py", title="Search"),
    st.Page("pages/ask.py", title="Ask Assistant"),
    st.Page("pages/analytics.py", title="Analytics"),
]

pg = st.navigation(pages)
apply_custom_styles()
pg.run()
