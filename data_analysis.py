import pandas as pd 

df=pd.read_csv("students.csv")

print("\nFull Data:\n")
print(df)

print("\nAverage Marks:")
print(df['marks'].mean())

print("\nTop Student:")
top=df[df['marks']==df["marks"].max()]
print(top)

print("\n Last Student: ")
last=df[df['marks']==df['marks'].min()]
print(last)