from datetime import datetime, timedelta

class CalendarHelpers:
    @staticmethod
    def get_previous_day():
        today = datetime.today()
        yesterday = (today - timedelta(days=1)).date()
        return (yesterday.day,yesterday.month,yesterday.year)