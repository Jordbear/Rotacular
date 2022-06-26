import pandas as pd
import random

timetable = pd.read_csv('test.tsv', sep='\t', index_col='date')
staff = list(timetable.columns)
print(staff)
timetable = timetable.fillna(int(0)).astype(int)
timetable.index = pd.to_datetime(timetable.index, dayfirst=True)
timetable['Weekday'] = timetable.index.weekday
print(timetable)
print(timetable.dtypes)
for index, row in timetable[staff].iterrows():
    if row.sum() < 1:
        timetable.loc[index, random.choice(staff)] += 1
print(timetable)