import streamlit as st
from snowflake.snowpark.context import get_active_session
from common.build_table import load_access_table
from common.utils import check_role

# Set page layout to wide
st.set_page_config(layout="wide", page_title="Oppdater tilganger")

# Get the current credentials
session = get_active_session()
check_role(session)

st.title("Oppdater tilganger")
st.markdown("Trykk 'Oppdater' for å oppdatere tilganger til MicroStrategy (MSTR). ")
st.markdown("Merk: dersom man ikke klikker 'Oppdater' under så vil eventuelle endringer i grupper, kostnadsstedsrelasjoner og oppgaverelasjoner bli lagret i Snowflake, men *ikke* bli sendt til MSTR.")


update_data = st.button("Oppdater")

if update_data:
    try:
        load_access_table(session=session)
        st.success('Suksess!', icon="✅") 
    except Exception as e:
        st.error(e, icon="🚨")


