from source.sql.main import SQLmain as sql
from source.sql.tables import MainTable

print(sql.get_data_on_user_id(table=MainTable, user_id='1660717258'))
