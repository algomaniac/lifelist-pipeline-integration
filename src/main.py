# -*- coding: utf-8 -*-

import os

import trellohelper
import constants

from trello.exceptions import *
from confluence_helper import update_lifelist_page,get_lifelist_page_contents

from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader = PackageLoader('main', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def generate_lifelist_xhtml(trello_data):  
    template = env.get_template('page.xhtml')

    return template.render(data=trello_data,domains=constants.project_domains) #,domain_prefixes=constants.reverse_project_domain_map


def main():
    try:
        
        get_lifelist_page_contents()
        print('done')
        exit()

        data = trellohelper.get_pipeline_data()   

        xhtml = generate_lifelist_xhtml(data)

        #print(xhtml)

        update_lifelist_page(xhtml)

        print('Done')


    except Unauthorized :
        print('Trello declined the request as unauthorized. Check the token and other credentials')
        exit()
    except ResourceUnavailable as e :
        print(str(e))
        exit()


if __name__ == '__main__':
    main()
