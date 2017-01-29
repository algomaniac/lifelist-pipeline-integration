import datetime


months = [None,'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def current_month_year():
    now = datetime.datetime.now()
    return (now.month,now.year)

def increment_month(month,year):
    global months

    if(month + 1 > 12):
        return (1,year+1)
    else:
        return(month + 1,year)

def month_year_tostring(month,year):
    global months

    return months[month] + ' ' + str(year)

def cmp_month_year(start_month_year,end_month_year):
    return 1 if ( start_month_year[1] < end_month_year[1] or ( start_month_year[1] == end_month_year[1] and start_month_year[0] < end_month_year[0 ]) ) else 0