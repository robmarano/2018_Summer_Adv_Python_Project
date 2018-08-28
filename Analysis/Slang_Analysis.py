import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import pandas as pd
import numpy as np
import datetime

df=pd.read_csv('C:/Users/vm555/Downloads/slang_big.csv', header=0, names=['index', 'state', 'keyword', 'time'], sep=',', index_col=0, encoding='utf8')

df1=df[df['state'].notnull()]
df1['time']=pd.to_datetime(df1['time'], format='%a %b %d %H:%M:%S +%f %Y')
df1['time']=df1['time'].dt.round('60min')
df2=df1.groupby(['time', 'state', 'keyword']).size().reset_index()
df2.columns = ['Time', 'State', 'Key Word', 'Word Count']

# Word Count for Lit
df3=df2[df2['Key Word']=='lit']
df3=df3.groupby(['State'])['Word Count'].sum().reset_index()
df3.hist()
df3.set_index('State')['Word Count'].plot.bar(figsize=(20, 5))
plt.title('Words Count For "Lit" Word')
plt.ylabel('Words Count')
plt.savefig('C:/Users/vm555/Documents/fig1.png')

# Word Count for Ratchet
df4=df2[df2['Key Word']=='ratchet']
df4=df4.groupby(['State'])['Word Count'].sum().reset_index()
df4.hist()
df4.set_index('State')['Word Count'].plot.bar(figsize=(20, 5))
plt.title('Words Count For "Ratchet" Word')
plt.ylabel('Words Count')
plt.savefig('C:/Users/vm555/Documents/fig2.png')

# Word Count for Adulting
df5=df2[df2['Key Word']=='adulting']
df5=df5.groupby(['State'])['Word Count'].sum().reset_index()
df5.hist()
df5.set_index('State')['Word Count'].plot.bar(figsize=(20, 5))
plt.title('Words Count For "Adulting" Word')
plt.ylabel('Words Count')
plt.savefig('C:/Users/vm555/Documents/fig3.png')
