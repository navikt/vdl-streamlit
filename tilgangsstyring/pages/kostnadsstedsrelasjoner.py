import streamlit as st
from snowflake.snowpark.context import get_active_session


# Get the current credentials
session = get_active_session()

# Check if user has the required role
session.use_role("TILGANGSSTYRING_REPORTER")

st.title("Kostnadsstedsrelasjoner")

left, right = st.columns(2)


right.write(
    """
    Legge til en kostnadsstedsrelasjon
    """
)


with right.form("Legg til kostnadsstedsrelasjon"):
    available_groups_statement = f"""
            SELECT gruppe FROM grupper WHERE _slettet_dato is null
        """
    df_available_groups = session.sql(available_groups_statement).to_pandas()
    available_cost_centre_statement = f"""
            SELECT kostnadssted FROM gyldig_kostnadssted_liste ORDER BY 1
        """
    df_available_cost_centre = session.sql(available_cost_centre_statement).to_pandas()
    group = st.selectbox("Velg gruppe",df_available_groups)
    cost_centre = st.selectbox("Velg kostnadssted",df_available_cost_centre)
    submit_group = st.form_submit_button('Legg til kostnadsstedsrelasjon')
    
if submit_group:
    exists_statement = f"""
        SELECT * 
        FROM gruppe_kostnadssted_relasjoner 
        WHERE gruppe = upper('{group}') 
          AND kostnadssted = '{cost_centre}' 
          AND _slettet_dato is null 
    """
    df_exists = session.sql(exists_statement).to_pandas()
    if df_exists.empty:
        insert_statment=f"""
            INSERT INTO gruppe_kostnadssted_relasjoner (
                gruppe,
                kostnadssted,
                _opprettet_av,
                _opprettet_dato, 
                _oppdatert_av,
                _oppdatert_dato
            ) VALUES (
                upper('{group}'),
                '{cost_centre}',
                '{st.experimental_user["email"]}',
                current_date, 
                '{st.experimental_user["email"]}',
                current_date 
            )
        """
        session.sql(insert_statment).collect()
        right.success('Suksess!', icon="✅") 
    else:
        right.error('Kostnadsstedsrelasjonen eksisterer allerede', icon="🚨")

right.write(
    """
    Slette en kostnadsstedsrelasjon
    """
)
with right.form("Slett Gruppe"):
    groups_for_delete_statement = f"""
            SELECT gruppe 
            FROM gruppe_kostnadssted_relasjoner 
            WHERE _slettet_dato is null 
            ORDER BY 1
        """
    df_groups_for_delete = session.sql(groups_for_delete_statement).to_pandas()
    group = st.selectbox("Velg gruppe",df_groups_for_delete)
    cost_centre_for_delete_statement = f"""
            SELECT kostnadssted 
            FROM gruppe_kostnadssted_relasjoner
            WHERE _slettet_dato is null 
              AND gruppe = '{group}'
            ORDER BY 1
        """
    df_cost_centre_for_delete = session.sql(cost_centre_for_delete_statement).to_pandas()
    cost_centre = st.selectbox("Velg kostnadssted",df_cost_centre_for_delete)
    delete_group = st.form_submit_button('Slett kostnadsstedsrelasjon')

if delete_group:
    delete_statment=f"""
        update gruppe_kostnadssted_relasjoner set 
            _oppdatert_av = '{st.experimental_user["email"]}',
            _oppdatert_dato = current_date, 
            _slettet_dato = current_date
        where gruppe = upper('{group}')
        and kostnadssted = '{cost_centre}'
        """
    session.sql(delete_statment).collect()
    right.success('Suksess!', icon="✅")  
    # st.rerun()

left.write(
    """
    Oversikt over alle kostnadsstedsrelasjoner
    """
)
gruppe_view = f"""
    SELECT 
        grp.gruppe, 
        grp.kostnadssted,
        ksted.kostnadssted_navn
    FROM gruppe_kostnadssted_relasjoner grp 
    JOIN gyldig_kostnadssted_liste ksted on ksted.kostnadssted = grp.kostnadssted 
    WHERE _slettet_dato IS NULL 
    """
df_groups = session.sql(gruppe_view).to_pandas()
left.dataframe(df_groups, on_select="rerun", hide_index=True, use_container_width=True)