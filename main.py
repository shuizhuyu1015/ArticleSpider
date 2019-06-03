"""
    create by Gray 2019-05-20
"""

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# try:
# execute(['scrapy', 'crawl', 'jobbole'])
# execute(['scrapy', 'crawl', 'jiuyi160'])
execute(['scrapy', 'crawl', 'codingke'])

# finally:
# ExportExcel.export()
