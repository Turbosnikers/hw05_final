import datetime as dt

date_now = dt.datetime.now()


def year(request):
    """Добавляет переменную с текущим годом."""
    return {
        'year': int(date_now.strftime("%Y"))
    }
