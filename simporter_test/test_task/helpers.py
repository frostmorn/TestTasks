import datetime
from . import db
def get_next_grouping_date(date, grouping):
    if grouping == 'weekly':
        return date + datetime.timedelta(days=7)
    elif grouping == 'bi-weekly':
        return date + datetime.timedelta(days=14)
    elif grouping == 'monthly':
        next_month = date.month + 1 if date.month != 12 else 1
        next_date = datetime.datetime(year = date.year, month = next_month, day = 1, hour = date.hour, 
            minute = date.minute, second = date.second, microsecond = date.microsecond)  # just in case
        return next_date
    else:
        raise ValueError("Unknown grouping type specified")

def get_table_columns(table="data", ignore_columns = ['id', 'timestamp']):
    filter_list = []
    columns = []

    cached_key = "C"+str(hash(table + "".join(ignore_columns)))
    # if scheme changed we need to reload
    # default flask g clears at the end of request
    if 'table_cache' not in globals():
        global table_cache
        table_cache = {}
        print("Creating table_cache")

    if not(cached_key in table_cache):

        for column in ignore_columns:
            filter_list.append(" name <> \"{column}\" ".format(column = column))

        if len(ignore_columns) > 0:
            request_columns = "SELECT name from pragma_table_info(\"{table}\") WHERE {filter}".format(table = table, filter = "AND".join(filter_list))
        else:
            request_columns = "select name from pragma_table_info(\"{table}\");".format(table = table)

        database = db.get_db()
        columns = database.execute(request_columns).fetchall()

        columns = list(map(lambda row: row[0], columns))
        
        table_cache[cached_key] = columns

    return table_cache[cached_key]
