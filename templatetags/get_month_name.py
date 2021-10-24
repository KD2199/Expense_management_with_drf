
import calendar


def get_month(name):
    """
       return month name from month number
    """
    if name < '10':
        name = name[1]
    name = calendar.month_name[int(name)]
    
    return name

