from urllib import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pyodbc
import os

def create_session():
    db_pwd = os.environ.get("DB_PASSWORD")
    driver = "{ODBC Driver 18 for SQL Server}"
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:acdcpiratedb.database.windows.net,1433;Database=acdcpirate;Uid=captain;Pwd=AcDc2023;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    params = parse.quote_plus(connection_string)

    engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(connection_string))
    session = Session(engine)
    return session

