from datetime import date, time, datetime

def timetable(dates, times):
    try:
        datetimes = []
        for date in dates:
            for time in times:
                new_datetime = datetime.combine(date, time)
                datetimes.append(new_datetime)
    except:
        raise Exception
            
    return sorted(datetimes)
