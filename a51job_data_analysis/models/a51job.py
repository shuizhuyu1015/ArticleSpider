"""
    Create by GL on 2019-08-01
"""
import datetime
from collections import Counter

import pymysql


class A51job:
    def __init__(self):
        dbparas = dict(
            host='localhost',
            port=3306,
            db='article_spider',
            user='root',
            passwd='123456',
            charset='utf8mb4'
        )
        self.db_conn = pymysql.connect(**dbparas)
        self.db_cur = self.db_conn.cursor()

    # 查询行业及发布的职位数量
    def query_industry(self):
        industry_sql = """
            SELECT industryField FROM 51job_python;
        """
        # 执行sql语句
        self.db_cur.execute(industry_sql)

        # 获取查询数据
        # <class 'tuple'>: ('互联网/电子商务,多元化业务集团公司',)
        # <class 'tuple'>: ('计算机服务(系统、数据服务、维修),互联网/电子商务',)
        # <class 'tuple'>: ('通信/电信/网络设备',)
        processed_result = []
        for i in self.db_cur.fetchall():
            # 数据库查询到的数据格式多样，需多次分割替换
            indus = i[0].split(',')[0].split('/')[0]
            indus = indus.replace('互联网', '电子商务')
            indus = indus.split('(')[0]
            processed_result.append(indus)

        # 填充series里的data
        # Counter计数，并判断数量大于1000的才返回
        data = [{'name': k, 'value': v} for k, v in Counter(processed_result).items() if v > 1000]
        name_list = [i_dic['name'] for i_dic in data]

        info = {
            'x_name': name_list,
            'data': data
        }
        return info

    # 查询薪资
    def query_salary(self):
        salary_sql = """
            SELECT salary FROM 51job_python;
        """
        self.db_cur.execute(salary_sql)

        # <class 'tuple'>: ('1.0-1.5万/月',)
        res = [i[0].split('/')[0] for i in self.db_cur.fetchall() if i[0]]

        data = [{'name': k, 'value': v} for k, v in Counter(res).items() if v > 1100]
        name_list = [i_dic['name'] for i_dic in data]

        info = {
            'x_name': name_list,
            'data': data
        }
        return info

    # 查询工作经验
    def query_work_year(self):
        work_year_sql = """
            SELECT workYear FROM 51job_python;
        """
        self.db_cur.execute(work_year_sql)

        res = [i[0] for i in self.db_cur.fetchall()]

        data = [{'name': k.replace('经验', ''), 'value': v} for k, v in Counter(res).items()]
        name_list = [i_dic['name'] for i_dic in data]

        info = {
            'x_name': name_list,
            'data': data
        }
        return info

    # 查询学历要求
    def query_education(self):
        education_sql = """
            SELECT education FROM 51job_python;
        """
        self.db_cur.execute(education_sql)

        res = [i[0] for i in self.db_cur.fetchall() if '招' not in i[0]]

        data = [{'name': k, 'value': v} for k, v in Counter(res).items() if v > 50]
        name_list = [i_dic['name'] for i_dic in data]

        info = {
            'x_name': name_list,
            'data': data
        }
        return info

    # 查询公司类型（合资、民营、国企等）
    def query_finance_stage(self):
        finance_sql = """
            SELECT financeStage FROM 51job_python;
        """
        self.db_cur.execute(finance_sql)

        res = [i[0] for i in self.db_cur.fetchall() if i[0]]

        data = [{'name': k, 'value': v} for k, v in Counter(res).items() if v > 1000]
        name_list = [i_dic['name'] for i_dic in data]

        info = {
            'x_name': name_list,
            'data': data
        }
        return info

    # 公司规模
    def query_company_size(self):
        company_size_sql = """
            SELECT companySize FROM 51job_python;
        """
        self.db_cur.execute(company_size_sql)

        res = [i[0] for i in self.db_cur.fetchall() if i[0]]

        data = [{'name': k, 'value': v} for k, v in Counter(res).items() if v > 1000]
        name_list = [i_dic['name'] for i_dic in data]

        info = {
            'x_name': name_list,
            'data': data
        }
        return info

    # 城市分布
    def query_city(self):
        city_sql = """
            SELECT city FROM 51job_python;
        """
        self.db_cur.execute(city_sql)

        res = [i[0].split('-')[0] for i in self.db_cur.fetchall() if i[0]]

        data = [{'name': k, 'value': v} for k, v in Counter(res).items()]
        name_list = [i_dic['name'] for i_dic in data]

        info = {
            'x_name': name_list,
            'data': data
        }
        return info

    # 抓取数量
    def job_count(self):
        all_sql = """
            SELECT positionID FROM 51job_python;
        """
        all_count = self.db_cur.execute(all_sql)

        today_sql = """
            SELECT * FROM 51job_python WHERE crawl_date=%s;
        """
        # yesterday = datetime.date.today() + datetime.timedelta(days=-1)
        today_count = self.db_cur.execute(today_sql, datetime.date.today())

        info = {
            'all_count': all_count,
            'today_count': today_count
        }
        return info


db_51job = A51job()
# db_51job.query_industry()
# db_51job.query_salary()
# db_51job.query_education()
# db_51job.query_finance_stage()
# db_51job.query_company_size()
