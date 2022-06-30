import pandas as pd
import math
import random

timetable = pd.read_csv('test.tsv', sep='\t', index_col='date')
staff = list(timetable.columns)
shifts_per_staff = math.floor((len(timetable.index) * 3) / len(staff))
remaining_shifts = (len(timetable.index) * 3) % len(staff)
staff_shifts = {i: shifts_per_staff for i in staff}
for i in random.sample(staff, remaining_shifts):
    staff_shifts[i] += 1
timetable['Weekday'] = pd.to_datetime(timetable.index, dayfirst=True).weekday
staff_shifts = list(staff_shifts.items())
random.shuffle(staff_shifts)
staff_shifts = dict(staff_shifts)

for index, row in timetable[staff].iterrows():
    available_staff = list(timetable[staff].columns[timetable[staff].loc[index].isna()])
    unassigned_staff = {k: v for k, v in staff_shifts.items() if k in available_staff and v > 0}
    unassigned_staff_list = list(unassigned_staff.items())
    random.shuffle(unassigned_staff_list)
    unassigned_staff = dict(unassigned_staff_list)
    if 'Early' not in row:
        chosen_staff = max(unassigned_staff, key=unassigned_staff.get)
        timetable.loc[index, chosen_staff] = 'Early'
        staff_shifts[chosen_staff] -= 1
    available_staff = list(timetable[staff].columns[timetable[staff].loc[index].isna()])
    unassigned_staff = {k: v for k, v in staff_shifts.items() if k in available_staff and v > 0}
    unassigned_staff_list = list(unassigned_staff.items())
    random.shuffle(unassigned_staff_list)
    unassigned_staff = dict(unassigned_staff_list)
    if 'Late' not in row:
        chosen_staff = max(unassigned_staff, key=unassigned_staff.get)
        timetable.loc[index, chosen_staff] = 'Late'
        staff_shifts[chosen_staff] -= 1
    available_staff = list(timetable[staff].columns[timetable[staff].loc[index].isna()])
    unassigned_staff = {k: v for k, v in staff_shifts.items() if k in available_staff and v > 0}
    unassigned_staff_list = list(unassigned_staff.items())
    random.shuffle(unassigned_staff_list)
    unassigned_staff = dict(unassigned_staff_list)
    if 'Night' not in row:
        chosen_staff = max(unassigned_staff, key=unassigned_staff.get)
        timetable.loc[index, chosen_staff] = 'Night'
        staff_shifts[chosen_staff] -= 1
print(timetable)
print(timetable.dtypes)

timetable.to_csv('output.tsv', sep='\t')
