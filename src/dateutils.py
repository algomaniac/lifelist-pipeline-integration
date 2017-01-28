

months = [None,'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def increment_month(month,year):
    global months

    if(month + 1 > 12):
        return (1,year+1)
    else:
        return(month + 1,year)

def month_year_tostring(month,year):
    global months

    return months[month] + ' ' + str(year)