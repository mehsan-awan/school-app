import pandas as pd

df= pd.read_csv('data.csv',index_col=0)
print(df)
df = df.set_index("Name")

#df.set_index("Admission No")
df=df.sort_index()
#df.drop([25], inplace = True)
print(df)