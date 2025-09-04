import sys

# مسیر پروژه (همه فایل‌ها در /home/hooshmand قرار دارند)
project_home = '/home/hooshmand'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# وارد کردن Flask app
from main import app as application
