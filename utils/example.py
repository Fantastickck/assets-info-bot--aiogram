from calendar import month
from datetime import datetime, timedelta, date

from dateutil.relativedelta import relativedelta

from emoji import emojize

# import datetime
# import dateutil.relativedelta
date_today = datetime.today()
# d = datetime.strptime("2013-03-31", "%Y-%m-%d")
print(date_today)
d2 = datetime.today() - relativedelta(years=1)
print(d2)

