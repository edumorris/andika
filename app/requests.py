import urllib.request, json
from .models import Quotes

base_url = None

def configure_request(app):
    global base_url
    base_url = 'http://quotes.stormconsultancy.co.uk/random.json'

def get_quote():
    '''
    Get random quote from Quotes API
    '''
    base_url = 'http://quotes.stormconsultancy.co.uk/random.json'

    with urllib.request.urlopen(base_url) as url_resp:
        quote_data = url_resp.read()
        quote_response = json.loads(quote_data)

        q_data = None

        if quote_response['quote']:
            quote = quote_response['quote']
            # q_data = process_results(quote_response)
    
    return quote

def process_results(result_input):
    '''
    Gets list of object
    '''

    quote_arr = []
    for quote_json in result_input:
        id = quote_json.get('id')
        author = quote_json.get('author')
        quote = quote_json.get('quote')
        link = quote_json.get('permalink')

        if quote:
            new_quote = Quotes(id, author, quote, link)
            quote_arr.append(new_quote)
        
        return quote_arr