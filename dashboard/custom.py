import streamlit as st


def apply_custom_styles():
    st.markdown(
        """
        <style>
        /* Ancho del sidebar */
        [data-testid="stSidebar"] {
            min-width: 250px;
            max-width: 250px;
        }
        
        /* Borde derecho del sidebar */
        [data-testid="stSidebar"] {
            border-right: 2px solid #10B981;
        }
        
        /* Tamaño del texto de navegación */
        [data-testid="stSidebarNav"] span {
            font-size: 18px !important;
        }
        
        /* Color del link activo */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            color: #10B981;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
