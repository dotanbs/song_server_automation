import requests as r
base_url = 'http://127.0.0.1:3002/'


def post(url, body):
    try:
        response = r.post(base_url + url, json=body)
        if response.status_code > 201:
            raise Exception("expected to get status code 20X, but get " + response.status_code)
        else:
            return response.json()
    except Exception as error:
        print('Caught this error: ' + repr(error))


def put(url, body):
    try:
        response = r.put(base_url + url, json=body)
        if response.status_code > 201:
            raise Exception("expected to get status code 20X, but get " + response.status_code)
        else:
            return response.json()
    except Exception as error:
        print('Caught this error: ' + repr(error))


def delete(url):
    try:
        response = r.delete(base_url + url)
        if response.status_code > 201:
            raise Exception("expected to get status code 20X, but get " + response.status_code)
        else:
            return response.json()
    except Exception as error:
        print('Caught this error: ' + repr(error))


def get(url):
    try:
        response = r.get(base_url + url)
        if response.status_code > 201:
            raise Exception("expected to get status code 20X, but get " + response.status_code)
        else:
            return response.json()
    except Exception as error:
        print('Caught this error: ' + repr(error))
