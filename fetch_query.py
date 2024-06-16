from sqlalchemy import create_engine,text
import pandas as pd

def query_fetch(roundrace):
    connection_string =  "mysql+mysqlconnector://root:prisonreform@localhost:3306/f1db2024"
    engine = create_engine(connection_string, echo=True)
    lapquery = f"SELECT * FROM laptimes T0 WHERE T0.Race = '{roundrace}'"
    driverquery = "SELECT * FROM driver_master T0"
    minisecquery = f"SELECT * FROM minisec_master T0 WHERE T0.Race = '{roundrace}'"
    telemetryquery = f"SELECT * FROM minisecspeed T0 WHERE T0.Race = '{roundrace}'"
    lapdf = pd.read_sql(sql=lapquery,con=engine)
    driver_df = pd.read_sql(sql=driverquery,con=engine)
    minisec_mast = pd.read_sql(sql=minisecquery,con=engine)
    tele_df = pd.read_sql(sql=telemetryquery,con=engine)
    driver_num = driver_df['Driver']
    driver_df = driver_df.drop('Driver',axis=1)
    driver_df.insert(0, 'Driver', driver_num)
    lapdf['Driver_Num'] = lapdf['Driver_Num'].astype(int)
    speedf = pd.merge(lapdf,driver_df,how='inner',left_on = 'Driver_Num',right_on = 'Driver')
    speedf = speedf.drop('Driver',axis=1)
    minisecspeed = pd.merge(tele_df,driver_df, how = 'left', left_on = 'DriverNumber', right_on = 'Driver')
    df_dict = {'Laptimes':speedf,'MSECAVG':minisecspeed,'MSEC':minisec_mast}
    return df_dict
