from datetime import datetime, date, timedelta
d = date.today()
s = "20"+d.strftime("%y%m%d")+"120000"
day = timedelta(days=1)
new = d+day

start_time = "20" + (date.today()-timedelta(days=1)).strftime("%y%m%d") + "120000"
print d, s, day, new, start_time
