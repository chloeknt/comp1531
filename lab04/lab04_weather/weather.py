from datetime import datetime
import csv

def weather(date, location):
    date_object = datetime.strptime(date, '%d-%m-%Y')
    
    count = 0
    total_min = 0
    total_max = 0
    
    # find the average min and max across all time at that location
    with open("weatherAUS.csv", "r", encoding = "ascii") as csv_file:
        csvreader = csv.reader(csv_file)
        for row in csvreader:
            if count == 0:
                count += 1
            elif valid(row) and row[1] == location:
                total_min += float(row[2])
                total_max += float(row[3])
                count += 1
    avg_min = total_min / (count - 1)
    avg_max = total_max / (count - 1)

    min_res = 0
    max_res = 0
    count = 0
    found = False

    with open("weatherAUS.csv", "r", encoding = "ascii") as csv_file:
        # find the specific day's values
        csvreader = csv.reader(csv_file)
        for row in csvreader:
            if count == 0:
                count += 1
            elif datetime.strptime(row[0], '%Y-%m-%d') == date_object and row[1] == location:
                if row[2] != 'NA':
                    min_res = round(avg_min - float(row[2]), 1)
                else:
                    min_res = None
                if row[3] != 'NA':
                    max_res = round(float(row[3]) - avg_max, 1)
                else:
                    max_res = None
                found = True

    if found == False:
        raise Exception("Invalid date or location")

    return (min_res, max_res)
    
def valid(row):
    if row[2] != 'NA' and row[3] != 'NA':
        return True
    return False
