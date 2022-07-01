import pandas as pd
import math
import random

timetable = pd.read_csv('test.tsv', sep='\t', index_col='date')
staff = list(timetable.columns)
timetable['Weekday'] = pd.to_datetime(timetable.index, dayfirst=True).weekday
shifts_per_staff = math.floor(len(timetable.index) / len(staff))
remaining_earlys = remaining_lates = remaining_nights = len(timetable.index) % len(staff)
staff_shifts = {i: [shifts_per_staff, shifts_per_staff, shifts_per_staff] for i in staff}
shifts_table = pd.DataFrame.from_dict(staff_shifts, orient='index')


def add_remaining(column, remaining_shifts):
    total_shifts = shifts_table.sum(axis=1)
    least_shifts = total_shifts[total_shifts == total_shifts.min()].index.values.tolist()
    most_shifts = [i for i in staff if i not in least_shifts]
    if len(least_shifts) > remaining_shifts:
        added_staff = random.sample(least_shifts, remaining_shifts)
    elif len(least_shifts) == remaining_shifts:
        added_staff = least_shifts
    elif len(least_shifts) < remaining_shifts:
        added_staff = least_shifts + random.sample(most_shifts, remaining_shifts - len(least_shifts))
    for i in added_staff:
        shifts_table.loc[i, column] += 1


add_remaining(0, remaining_earlys)
add_remaining(1, remaining_lates)
add_remaining(2, remaining_nights)

print(shifts_table)

early_shifts = shifts_table[0].to_dict()
late_shifts = shifts_table[1].to_dict()
night_shifts = shifts_table[2].to_dict()


def assign_staff(shift, shift_numbers):
    available_staff = list(timetable[staff].columns[timetable[staff].loc[index].isna()])
    unassigned_staff = {k: v for k, v in shift_numbers.items() if k in available_staff and v > 0}
    unassigned_staff_list = list(unassigned_staff.items())
    random.shuffle(unassigned_staff_list)
    unassigned_staff = dict(unassigned_staff_list)
    if shift not in row:
        # print(timetable)
        # print(shift_numbers)
        # print(available_staff)
        # print(unassigned_staff)
        chosen_staff = max(unassigned_staff, key=unassigned_staff.get)
        timetable.loc[index, chosen_staff] = shift
        shift_numbers[chosen_staff] -= 1


for index, row in timetable[staff].iterrows():
    assign_staff('Early', early_shifts)
    assign_staff('Late', late_shifts)
    assign_staff('Night', night_shifts)

print(timetable)

timetable.to_csv('output.tsv', sep='\t')
