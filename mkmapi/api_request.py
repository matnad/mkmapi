from oauthlib.oauth1.rfc5849 import Client
from requests import request

from mkmapi.env_variables import (
    get_mkm_app_token,
    get_mkm_app_secret,
    get_mkm_access_token,
    get_mkm_access_token_secret,
    get_mkm_base_url,
)
from mkmapi.exceptions import MKMConnectionError
from mkmapi.mkm_oauth1_client import MKMClient
from mkmapi.mkm_oauth1_serializer import MKMOAuth1


class ApiRequest:

    def __init__(self, app_token=None, app_secret=None, access_token=None, access_token_secret=None, is_sandbox=False):
        """
        Initializes the endpoint used for requests.

        :param app_token: Token for the app
        :param app_secret:  Secret for the app
        :param access_token: Authentication token
        :param access_token_secret: Secret for authentication token
        :param is_sandbox: True to connect to sandbox endpoint, False for production endpoint
        """
        self.base_endpoint = get_mkm_base_url(is_sandbox)
        self.app_token = app_token if app_token is not None else get_mkm_app_token()
        self.app_secret = app_secret if app_secret is not None else get_mkm_app_secret()
        self.access_token = access_token if access_token is not None else get_mkm_access_token()
        self.access_token_secret = access_token_secret \
            if access_token_secret is not None else get_mkm_access_token_secret()

    def request(self, url, method, params, **kwargs):
        """
        Sends requests to the server with parameters passed.

        :param url: URL where the request is submitted
        :param method: Method used for the request
        :param params: Query parameters for the request
        :param kwargs: Optional additional parameters such as body
        :return: Returns the response received from the server
        """

        complete_url = f'{self.base_endpoint}{url}'
        auth = self.create_auth(complete_url)
        print(method, complete_url, auth, params, kwargs)
        response = request(method=method, url=complete_url, auth=auth, params=params, **kwargs)
        return self.handle_response(response)

    def create_auth(self, url):
        """
        Create authorization with MKMOAuth1, if Access Token and Access Token Secret
        are not found a custom Client is used.
        This is done because MKM expects an authorization header with certain parameters
        even if they're empty strings.

        :param url: URL where request is submitted
        :return: Returns an instance of `MKMOAuth1` with `url` as realm
        """

        # If access_token and access_token_secret are empty strings a personalized OAuth1 Client is used.
        # This is done because that would mean the user is using a Widget Application and having empty strings
        # as tokens causes issues with the default Client
        if not self.access_token and not self.access_token_secret:
            client = MKMClient
        else:
            client = Client
        return MKMOAuth1(self.app_token,
                         client_secret=self.app_secret,
                         resource_owner_key=self.access_token,
                         resource_owner_secret=self.access_token_secret,
                         client_class=client,
                         realm=url)

    @staticmethod
    def handle_response(response):
        """
        Check the HTTP response.

        :param response: Response received from the server
        :return: Returns the response received if positive or raise exception if negative
        """

        status = response.status_code
        if 200 <= status <= 299:
            return response
        else:
            raise MKMConnectionError(response)
