import requests, json

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from bridge_api.version import __version__


DEFAULT_TIMEOUT = 60
DEFAULT_LIMIT = 100


class Client(object):
    '''
    Python Bridge API client.

    '''

    def __init__(self, client_id, client_secret):
        '''
        Initialize a client with credentials.

        '''

        self.api_root = 'https://sync.bankin.com'
        self.client_id = client_id
        self.client_secret = client_secret

        self.Users = Users(self)
        self.Banks = Banks(self)
        self.Items = Items(self)
        self.Transactions = Transactions(self)

    def _http_request(self, url, method, data, timeout=DEFAULT_TIMEOUT):
        '''
        Prepare and make a http request to API

        '''

        headers_data = {
            'Bankin-Version': __version__,
            'Content-Type': 'application/json',
        }
        if data.get('access_token', None):
            headers_data.update(
                {'Authorization': 'Bearer %s'%data.pop('access_token')}
            )
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        if data.get('access_token_query', None):
            params.update({'access_token': data.pop('access_token_query')})
        params.update(data)
        try:
            params_data = urlencode(params)
        except Exception as e:
            raise e
        response = getattr(requests, method)(
            url,
            json={},
            params=params_data,
            headers=headers_data,
            timeout=timeout,
        )
        if response.text:
            try:
                response_body = json.loads(response.text)
            except ValueError:
                raise Exception({
                    'error_message': response.text,
                    'error_title': 'Request occured an error.',
                    'error_code': 'request_error',
                })
            if response_body.get('type'):
                raise Exception(response_body)
            else:
                return response_body
        else:
            return

    def get(self, path, data):
        '''
        Make a get request.

        '''

        url = urlparse.urljoin(self.api_root, path)
        return self._http_request(url, 'get', data)

    def post(self, path, data):
        '''
        Make a post request.

        '''

        url = urlparse.urljoin(self.api_root, path)
        return self._http_request(url, 'post', data)

    def put(self, path, data):
        '''
        Make a put request.

        '''

        url = urlparse.urljoin(self.api_root, path)
        return self._http_request(url, 'put', data)

    def delete(self, path, data):
        '''
        Make a delete request.

        '''

        url = urlparse.urljoin(self.api_root, path)
        return self._http_request(url, 'delete', data)


class API(object):
    '''
    Base class containing all other API endpoints.

    '''

    def __init__(self, client):
        self.client = client


class Users(API):
    '''
    Users endpoints.

    '''

    def create(self, email, password):
        '''
        Create a User

        '''

        data = {'email': email, 'password': password}
        return self.client.post('/v2/users', data)

    def authenticate(self, email, password):
        '''
        Authenticate a User

        '''

        data = {'email': email, 'password': password}
        return self.client.post('/v2/authenticate', data)

    def logout(self, access_token):
        '''
        User logout

        '''

        data = {'access_token': access_token}
        return self.client.post('/v2/logout', data)

    def list(self):
        '''
        Users list

        '''

        return self.client.get('/v2/users', {'limit': DEFAULT_LIMIT})

    def retrieve(self, uuid):
        '''
        Retrieve a User

        '''

        return self.client.get('/v2/users/%s'%uuid, {})

    def edit(self, uuid, current_password, new_password):
        '''
        Change User password

        '''

        data = {
            'current_password': current_password,
            'new_password': new_password
        }
        return self.client.put('/v2/users/%s/password'%uuid, data)

    def delete(self, uuid, password):
        '''
        Delete a User

        '''

        data = {'password': password}
        return self.client.delete('/v2/users/%s'%uuid, data)

    def delete_all(self):
        '''
        Delete all Users(works only for sandbox enviroment)

        '''

        return self.client.delete('/v2/users', {})


class Banks(API):
    '''
    Banks endpoints.

    '''

    def list(self):
        '''
        List of banks

        '''

        data = {'limit': DEFAULT_LIMIT}
        return self.client.get('/v2/banks', data)

    def retrieve(self, id):
        '''
        Retrieve a Bank

        '''

        return self.client.get('/v2/banks/%s'%id, {})


class Items(API):
    '''
    Items endpoints.

    '''

    def connect(self, bank_id, access_token, redirect_url=None):
        '''
        Connect an Item

        '''

        data = {
            'bank_id': bank_id, 'access_token': access_token,
            'redirect_url': redirect_url,
        }
        return self.client.post('/v2/items/connect', data)

    def list(self, access_token):
        '''
        Items list

        '''

        data = {'limit': DEFAULT_LIMIT, 'access_token': access_token}
        return self.client.get('/v2/items', data)

    def retrieve(self, uuid, access_token):
        '''
        Retrieve an Item

        '''

        data = {'access_token':access_token}
        return self.client.get('/v2/items/%s'%uuid, data)

    def status(self, uuid, access_token):
        '''
        Status of an Item

        '''

        data = {'access_token': access_token}
        return self.client.get('/v2/items/%s/status'%uuid, data)

    def refresh(self, uuid, access_token):
        '''
        Refresh an Item

        '''

        data = {'access_token': access_token}
        return self.client.post('/v2/items/%s/refresh'%uuid, data)

    def refresh_status(self, uuid, access_token):
        '''
        Refresh Status of an Item

        '''

        data = {'access_token': access_token}
        return self.client.get('/v2/items/%s/refresh'%uuid, data)

    def delete(self, uuid, access_token):
        '''
        Delete an Item

        '''

        data = {'access_token': access_token}
        return self.client.delete('/v2/items/%s'%uuid, data)


class Accounts(API):
    '''
    Accounts endpoints.

    '''

    def list(self, access_token):
        '''
        List of accounts

        '''

        data = {
            'limit': DEFAULT_LIMIT,
            'access_token': access_token
        }
        return self.client.get('/v2/accounts', data)

    def retrieve(self, id, access_token):
        '''
        Retrieve an Account

        '''

        data = {
            'access_token': access_token
        }
        return self.client.get('/v2/accounts/%s'%id, data)


class Transactions(API):
    '''
    Transactions endpoints.

    '''

    def list(self, until, access_token):
        '''
        List of transactions

        '''

        until = until.isoformat()
        data = {
            'limit': DEFAULT_LIMIT, 'until': until,
            'access_token': access_token
        }
        return self.client.get('/v2/transactions', data)

    def list_updated(self, since, access_token):
        '''
        List of updated transactions

        '''

        since = since.isoformat()
        data = {
            'limit': DEFAULT_LIMIT, 'since': since,
            'access_token': access_token
        }
        return self.client.get('/v2/transactions/updated', data)

    def retrieve(self, id, access_token):
        '''
        Retrieve an Account

        '''

        data = {
            'access_token': access_token
        }
        return self.client.get('/v2/transactions/%s'%id, data)
