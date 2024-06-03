import psycopg2
import cx_Oracle as cx
import pandas as pd
from sqlalchemy import types, create_engine
import warnings
warnings.filterwarnings('ignore')

def incremental_load(last_update):
    #Connection Configuration
    #Posgre
    conn_pg = psycopg2.connect(
        database="database", user='user123', password='post123', host='10.207.288.281', port= '5432'
    )

    cursor_pg = conn_pg.cursor()

    #EXTRACT DATA
    df_tr_news = pd.read_sql(f'''
        SELECT
        id, TO_CHAR(date_created,'YYYY/MM/DD HH24:MI:SS') date_created,  TO_CHAR(date_modified,'YYYY/MM/DD HH24:MI:SS') date_modified, title, "content", TO_CHAR(publication_date,'YYYY/MM/DD HH24:MI:SS') publication_date, author, category
        FROM TR_NEWS
        WHERE EXTRACT(YEAR FROM publication_date) = {last_update}
        ''', con=conn_pg
    )

    #TRANSFORM DATA
    columns_to_cast = ['date_created','date_modified','publication_date']

    for col in columns_to_cast:
        df_tr_news[col] = pd.to_datetime(df_tr_news[col]).astype('datetime64[s]') 

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
    connection_string = 'Shrpt/Shrpt23@10.207.231.214:1521/SHRRPT'
    connection_string1= 'oracle+cx_oracle://Shrpt:Shrpt23@10.207.231.214:1521/?service_name=SHRRPT'
    engine = create_engine(connection_string1)

    con = cx.connect(connection_string)
    cur = con.cursor()

    cur.execute("TRUNCATE TABLE STG_TR_NEWS")
    df_tr_news.to_sql('STG_TR_NEWS', con=engine, if_exists='append', index=False, dtype=dtype)

    con.commit()

    query_merge = '''MERGE INTO STAGING_TR_NEWS TGT USING(
            SELECT * 
            FROM STG_TR_NEWS) SRC ON (TGT.ID = SRC.ID)
    WHEN MATCHED THEN UPDATE SET 
            TGT.date_created = SRC.date_created , 
            TGT.date_modified = SRC.date_modified , 
            TGT.title = SRC.title ,
            TGT.content = SRC.content, 
            TGT.publication_date = SRC.publication_date , 
            TGT.author = SRC.author ,
            TGT.category = SRC.category 
    WHEN NOT MATCHED THEN 
    INSERT (TGT."ID", TGT.date_created, TGT.date_modified, TGT.title, TGT.content, TGT.publication_date, TGT.author,
            TGT.category) 
    VALUES (SRC."ID", SRC.date_created, SRC.date_modified, SRC.title, SRC.content, SRC.publication_date, SRC.author,
            SRC.category)'''

    cur.execute(query_merge)

    con.commit()
    con.close()

last_update = "2024"  # Contoh nilai waktu terakhir update
incremental_load(last_update)
