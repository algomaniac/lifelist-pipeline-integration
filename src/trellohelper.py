import sys
import os

from dateutils import current_month_year,increment_month,month_year_tostring,cmp_month_year

from trello import TrelloClient, Board, List, Card
from trello.exceptions import *
from trello.util import create_oauth_token

import constants

#Global Variables
trello_client = None


def fetch_completed_tasks(data):

    #Start from the earliest month
    curr_month_year = constants.start_month_year

    end_month_year = current_month_year()

    completed_entries = {}

    while(cmp_month_year(curr_month_year,end_month_year) == 1):
        entries = fetch_entries_by_list( 'Done - ' + month_year_tostring(*curr_month_year) , data )

        if(len(entries) > 0):
            completed_entries[month_year_tostring(*curr_month_year)] = entries

        curr_month_year = increment_month(*curr_month_year)

    return completed_entries


def fetch_entries_by_list(listname,data):

    # global project_categories
    # global category_labels
    # global client_labels

    all_lists = data['lists']
    all_cards = data['cards']

    all_entries = []

    try:
        curr_list_id = next(list.id for list in all_lists if list.name == listname)
    except StopIteration:
        #List does not exist
        return all_entries

    #for debugging
    cards_iterator = (x for x in all_cards if x.list_id == curr_list_id)

    for card in (x for x in all_cards if x.list_id == curr_list_id):

        entry_labels = None

        entry_client = None
        entry_category = None
        entry_domain = None
        entry_name = None

        try:
            entry_labels = card.list_labels
        except Exception:
            pass

        entry_domain,entry_name = card.name.split(':') if card.name.split(':')[0] in constants.project_domains.keys() else [None,card.name]
        
        if( entry_labels != None and len( entry_labels ) > 0 ):
            
            entry_client = entry_labels[1].name if ( len( entry_labels ) == 2 and entry_labels[1].name in constants.client_labels ) else entry_labels[0].name if entry_labels[0].name in constants.client_labels else ''
            entry_category = entry_labels[1].name if ( len( entry_labels ) == 2 and entry_labels[1].name in constants.category_labels ) else entry_labels[0].name if entry_labels[0].name in constants.category_labels else ''

            if(entry_client == 'Personal' and entry_category == 'Tasks'):
                #Personal Tasks will be ignored
                continue

        if(entry_domain == None and (entry_client == 'JDA Assigned')):
            #JDA Assigned stories will have prefix JDA
            entry_domain = 'STR'

        if(entry_category == 'Tasks'):
            #tasks will have prefix TASK
            entry_domain = 'TASK'

        if(entry_category == 'Blogpost'):
            #tasks will have prefix TASK
            entry_domain = 'BLOG'

        entry = { "name":str(entry_name),"category":str(entry_category),"client":str(entry_client),"domain":str(entry_domain),"closed":str(card.closed),"duedate":str(card.due),"status":listname}
        all_entries.append(entry)
    
    return all_entries

def get_pipeline_data():

    global trello_client

    pipeline_board = None
    all_labels = None
    all_lists = None
    all_cards = None

    #Generate access token
    #access_token = create_oauth_token()
    access_token = {'oauth_token':'6d465a2eca229f8db6be256c33422793110ed6a7ede184a10308d26a56372a59','oauth_token_secret':'b5223b272a653881c0568863094a2292'}

    #Initialize Trello client
    trello_client = TrelloClient(
        api_key=os.environ['TRELLO_API_KEY'],
        api_secret=os.environ['TRELLO_API_SECRET'],
        token = access_token['oauth_token'],
        token_secret=access_token['oauth_token_secret']
    )
    
    #Fetch Pipeline board
    pipeline_board = next(board for board in trello_client.list_boards(board_filter="open") if board.name == constants.pipeline_board_name)
    
    #Fetch all cards,labels & lists
    all_cards = pipeline_board.get_cards(filters='all',card_filter='all')
    all_labels = pipeline_board.get_labels()
    all_lists = pipeline_board.all_lists()

    board_data = {'cards':all_cards,'labels':all_labels,'lists':all_lists}

    #Write all cards to file
    # with open('allcards.txt','w') as f:
    #     f.write('[')
    #     for card in all_cards:
    #         card_json = trello_client.fetch_json('/cards/' + card.id)
    #         pprint(card_json, stream=f)
    #         f.write(',')
    #     f.write(']')
            

    infinite_task_queue = fetch_entries_by_list(listname='The Infinite Task Queue',data=board_data)    
    suspended_task_queue = fetch_entries_by_list(listname='Suspended',data=board_data)
    bucket_task_queue = fetch_entries_by_list(listname='Bucket',data=board_data)
    in_progress_task_queue = fetch_entries_by_list(listname='In Progress',data=board_data)
    completed_tasks_queue = fetch_completed_tasks(data=board_data)

    infinite_task_queue.reverse()

    return {
        "infinite_task_queue":infinite_task_queue,
        "suspended_task_queue":suspended_task_queue,
        "bucket_task_queue":bucket_task_queue,
        "in_progress_task_queue":in_progress_task_queue,
        "completed_tasks_queue":completed_tasks_queue
    }