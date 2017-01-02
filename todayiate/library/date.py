# -*- coding: utf-8

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "방금"
        if second_diff < 60:
            return str(second_diff) + "초 전"
        if second_diff < 120:
            return "1분 전"
        if second_diff < 3600:
            return str(second_diff / 60) + "분 전"
        if second_diff < 7200:
            return "한 시간 전"
        if second_diff < 86400:
            return str(second_diff / 3600) + "시간 전"
    if day_diff == 1:
        return "어제"
    if day_diff < 7:
        return str(day_diff) + "일 전"
    if day_diff < 31:
        return str(day_diff / 7) + "주 전"
    if day_diff < 365:
        return str(day_diff / 30) + "개월 전"
    return str(day_diff / 365) + "년 전"
