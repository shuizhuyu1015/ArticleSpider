"""
    create by Gray 2019-05-25
"""

import hashlib
from datetime import datetime
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def date_convert(value, loader_context):
    try:
        value = value.strip().replace('·', '').strip()
        create_date = datetime.strptime(value, loader_context.get('date_format', '')).date()
    except Exception as e:
        create_date = datetime.now().date()
    return create_date


def get_nums(value):
    reg_num = ".*?(\d+).*"
    match_re = re.match(reg_num, value.strip())
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums
