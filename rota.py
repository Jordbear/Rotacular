import pandas as pd

timetable = pd.read_csv('test.tsv', sep='\t', index_col='date')
staff = list(timetable.columns)
print(staff)
timetable.index = pd.to_datetime(timetable.index, dayfirst=True)
timetable['Weekday'] = timetable.index.weekday
print(timetable)
print(timetable.dtypes)
