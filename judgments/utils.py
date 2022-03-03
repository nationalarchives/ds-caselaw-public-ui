from datetime import datetime


def format_date(date):
    if date == "" or date is None:
        return None

    time = datetime.strptime(date, '%Y-%m-%d')
    return time.strftime('%d-%m-%Y')
