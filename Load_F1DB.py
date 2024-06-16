from sqlalchemy import create_engine,text
import numpy as np
import pandas as pd
from F1DB_Extract import ET_F1DB

roundrace = 'Canada'

def load_F1DB(roundrace):
    data = ET_F1DB(roundrace)
    lapsdf = data[0]
    driver_df = data[1]
    minisec = data[2]
    minisec_df = data[3]

    #Upload to Mysql DB using sqlalchemy
    connection_string =  "mysql+mysqlconnector://root:prisonreform@localhost:3306/f1db2024"
    engine = create_engine(connection_string, echo=True)
    lapsdf.to_sql('laptimes', con=engine, if_exists='append', index=False)
    driver_df.to_sql('driver_master', con=engine, if_exists='replace', index=False)
    minisec.to_sql('minisec_master', con=engine, if_exists='append', index=False)
    minisec_df.to_sql('minisecspeed', con=engine, if_exists='append', index=False)

load_F1DB(roundrace)