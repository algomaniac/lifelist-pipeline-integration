import os

from trello.exceptions import *

import trellohelper
from confluence_helper import update_lifelist_page


def generate_lifelist_xhtml(trello_data):
    pass


def main():
    try:
        data = trellohelper.get_pipeline_data()   

        xhtml = generate_lifelist_xhtml(data)

        update_lifelist_page(xhtml)


    except Unauthorized :
        print('Trello declined the request as unauthorized. Check the token and other credentials')
        exit()
    except ResourceUnavailable as e :
        print(str(e))
        exit()


if __name__ == '__main__':
    main()
