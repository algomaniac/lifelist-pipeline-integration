# -*- coding: utf-8 -*-

import os

import trellohelper
import constants
import dateutils

from trello.exceptions import *
from confluence_helper import update_lifelist_page,get_lifelist_page_contents

from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader = PackageLoader('main', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def generate_template_data(trello_data):
    template_data = {}

    template_data["infinite_task_queue"] = trello_data["infinite_task_queue"]
    template_data["bucket_task_queue"] = trello_data["bucket_task_queue"]
    template_data["in_progress_task_queue"] = trello_data["in_progress_task_queue"]
    template_data["suspended_task_queue"] = trello_data["suspended_task_queue"]

    template_data["domains"] = constants.project_domains
    template_data["completed_task_queue"] = []

    start_month_year = constants.start_month_year
    end_month_year = dateutils.current_month_year()

    while(dateutils.cmp_month_year(start_month_year,end_month_year) == 1):

        month_date_text = dateutils.month_year_tostring(*start_month_year)

        if(month_date_text not in trello_data["completed_tasks_queue"]):
            start_month_year = dateutils.increment_month(*start_month_year)
            continue

        result = {}
        result["month"] = month_date_text
        result["cards"] = trello_data["completed_tasks_queue"][month_date_text]

        #using insert so that latest month always comes at top of the list
        template_data["completed_task_queue"].insert(0,result)

        start_month_year = dateutils.increment_month(*start_month_year)

    return template_data

def generate_lifelist_xhtml(trello_data):

    #Generate template variables
    template_data = generate_template_data(trello_data)

    template = env.get_template('page.xhtml')

    return template.render(data=template_data) #,domain_prefixes=constants.reverse_project_domain_map


def main():
    try:

        data = trellohelper.get_pipeline_data()   

        xhtml = generate_lifelist_xhtml(data)

        #print(xhtml)

        update_lifelist_page(xhtml)

        print('Done')

        #Getting page contents
        # get_lifelist_page_contents()
        # print('done')
        # exit()


    except Unauthorized :
        print('Trello declined the request as unauthorized. Check the token and other credentials')
        exit()
    except ResourceUnavailable as e :
        print(str(e))
        exit()


if __name__ == '__main__':
    main()
