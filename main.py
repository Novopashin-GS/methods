from pymongo import MongoClient
from pprint import pprint
from pymongo import errors
from job_function import get_job_list


client = MongoClient('127.0.0.1', 27017)
db = client['job']
jobs = db.jobs
# 1 задание
job_list = get_job_list()
for job in job_list:
    try:
        jobs.insert_one(job)
    except errors.DuplicateKeyError:
        continue
for job in jobs.find({}):
    pprint(job)
# 2 задание


def get_job_more_input_salary(salary):
    result = jobs.find({'$or': [{'min_salary': {'$gte': salary}}, {'max_salary': {'$gte': salary}}]})
    for res in result:
        pprint(res)
