import pandas as pd






'''import pymysql as pim
from sqlalchemy import create_engine

enn=create_engine('mysql+pymysql://root:qwertyuiop[]@localhost/company')
conn=enn.connect()
'''

'''import mysql.connector as sqltor
conn=sqltor.connect(host="localhost",user="root",password="qwertyuiop[]",database="company")
print("yes" if conn.is_connected() else "NO")

conn.close()'''

d=pd.read_csv('sample-simple.csv',
              names=['a','b','c','d','m','f','g'],
              header=None
              )
print(d)