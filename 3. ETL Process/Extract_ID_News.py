import psycopg2
import cx_Oracle as cx
import pandas as pd
from sqlalchemy import types, create_engine
import warnings
warnings.filterwarnings('ignore')

#Connection Configuration
#Posgre
conn_pg = psycopg2.connect(
      database="dedb", user='postgres', password='postgres123', host='10.207.228.110', port= '5432'
)

cursor_pg = conn_pg.cursor()

#EXTRACT DATA
df_tr_news = pd.read_sql(f'''
    SELECT id
    FROM TR_NEWS
    ''', con=conn_pg
)

#TRANSFORM DATA

dtype = {} 
for j in df_tr_news.columns: 
    if (df_tr_news[j].dtype == 'object'): 
        if str(df_tr_news[j].str.len().max()) == 'nan': 
            dtype[j] = types.VARCHAR(30) 
        else : 
            dtype[j] = types.VARCHAR(df_tr_news[j].str.len().max()) 
    elif df_tr_news[j].dtype == 'float64': 
            dtype[j] = types.NUMERIC() 
    elif df_tr_news[j].dtype == 'datetime64[ns]': 
            dtype[j] = types.DATE()

#LOAD DATA
connection_string = 'user/password@localhost:1521/db'
connection_string1= 'oracle+cx_oracle://user:password@localhost:1521/?service_name=db'
engine = create_engine(connection_string1)

con = cx.connect(connection_string)
cur = con.cursor()

cur.execute("TRUNCATE TABLE ID_STAGING_TR_NEWS")
df_tr_news.to_sql('ID_STAGING_TR_NEWS', con=engine, if_exists='append', index=False, dtype=dtype)

con.commit()

con.commit()
con.close()
