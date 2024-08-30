# vdl-streamlit

## Hvor finner jeg Appen 
App for tilgangsstyring ligger [her](https://app.snowflake.com/qqhhrqv/finansiell_styring/#/streamlit-apps/TILGANGSSTYRING_RAW.USER_INPUT.TILGANGSSTYRING).

## Deploy av Streamlit app
Aktivere miljø:
```shell
. ./setup_env.sh
```
Deploy Streamlit til Snowflake fra ```/app```
```shell 
snow streamlit deploy --connection tilgangsstyring --replace
```
PS: her må Snowflake CLI connection objektet ```tilgangsstyring``` være definert ved å kjøre ```snow --info```og editere ```config.toml```-filen (dette må gjøres manuelt per nå).

# Deploy av app
Fra root kjør 
```
snowbird ru
snow sql -f app/tabeller_og_views.sql  --connection <connection>
cd app
snow streamlit deploy --connection <connection> --replace
snow sql -f post_hook.sql --connection <connection>
```


## TODOs
- Opprette tabeller, m.m. som streamlit appen trenger
    - view og __shared views__
- __Lage__ streamlit app 
- Snow CLI med Github actions
- __Lage__ dbt repo med ´row access policy´ macros
- Legge inn Snowflake CLI connection variabel som en del av miljøet? 


## Fjerning av Policies 
```sql
use database db; 
select distinct
'ALTER '||ref_entity_domain||
' '||ref_database_name||'.'||ref_schema_name||'.'||ref_entity_name||
' MODIFY COLUMN '||ref_column_name||
' UNSET MASKING POLICY;'
from table(information_schema.policy_references(policy_name=>'policies.<policy name>'));
```