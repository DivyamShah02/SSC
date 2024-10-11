import requests


base_url = 'http://127.0.0.1:8000/'

def sorter_api_call():
    url_endpoint = 'sort/'

    url = base_url + url_endpoint
    data = {
        'id':35
    }
    response = requests.post(url=url, data=data)

    print(response.text)

def property_api_call():
    url_endpoint = 'view-properties/'

    url = base_url + url_endpoint
    data = {
        'id':1
    }
    response = requests.post(url=url, data=data)

    print(response.text)


sorter_api_call()
# property_api_call()
