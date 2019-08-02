"""
    Create by GL on 2019-08-01
"""
from flask import Flask, render_template, json

from a51job_data_analysis.models.a51job import db_51job


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/51job')
def job_51():
    count_res = db_51job.job_count()
    return render_template('index.html', count_res=count_res)


@app.route('/get_echarts_data')
def get_echarts_data():
    info = {}
    info['echart_1'] = db_51job.query_industry()
    info['echart_2'] = db_51job.query_salary()
    info['echart_5'] = db_51job.query_work_year()
    info['echart_6'] = db_51job.query_education()
    info['echart_31'] = db_51job.query_finance_stage()
    info['echart_32'] = db_51job.query_company_size()
    info['map'] = db_51job.query_city()

    return json.dumps(info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
