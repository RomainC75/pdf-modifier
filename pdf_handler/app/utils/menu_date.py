from datetime import date, datetime
import re
import os

def date_checker(date_values:list):
    try:
        datetime(int(date_values[0]), int(date_values[1]), int(date_values[2]))
        return  True
    except:
        return False

# def get_date_of_today_or_last_day(sign_last_day_of_month):

#     today_date = date.today()
#     print(today_date)
#     last_day_converter = ['31','28','31','30','31','30','31','31','30','31','30','31']
#     day = None
#     if(sign_last_day_of_month):
#         day = last_day_converter[int(today_date.month)-1]
#     else:
#         day = str(today_date.day) if today_date.day>=10 else '0'+str(today_date.day)


def get_selected_date(date_selection_input):
    today_date = date.today()
    if date_selection_input == 'today':
        print("++++")
        day = str(today_date.day) if today_date.day>=10 else '0'+str(today_date.day)

    elif date_selection_input == 'default':
        last_day_converter = ['31','28','31','30','31','30','31','31','30','31','30','31']
        day = last_day_converter[int(today_date.month)-1]

    else:
        if re.search("^\d{4}-\d{2}-\d{2}$",date_selection_input):
            date_values = date_selection_input.split('-')
            if date_checker(date_values):
                return {
                    'day' : date_values[2],
                    'month' : date_values[1],
                    'year' : date_values[0]
                }

    return {
        'day' : day,
        'month' : str(today_date.month) if today_date.month>=10 else '0'+str(today_date.month),
        'year' : today_date.year
    }


