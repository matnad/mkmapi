from mkmapi.api_map.account_management import AccountManagement
from mkmapi.api_map.marketplace_info import MarketplaceInfo
from mkmapi.api_map.order_management import OrderManagement
from mkmapi.api_map.shopping_cart_manipulation import ShoppingCartManipulation
from mkmapi.api_map.stock_management import StockManagement
from mkmapi.api_map.wants_list_management import WantsListManagement
from mkmapi.api_request import ApiRequest
from mkmapi.mkm_xmlrequest_serializer import XMLSerializer


class Mkm:
    """Masterclass that holds all the API methods."""

    def __init__(self, app_token=None, app_secret=None, access_token=None, access_token_secret=None, sandbox=False):
        """
        Initializes the auth variables and specifies sandbox or production mode.
        Omitted auth vars will be loaded from the environment variables.
        If that fails, a MissingEnvVar Exception is thrown.

        :param app_token: App token for the app registered with the MKM account
        :param app_secret: Secret (key) for the app registered with the MKM account
        :param access_token: Access token for the MKM account
        :param access_token_secret: Secret (key) for the MKM account token
        :param sandbox: False (default) to use the production API, True to use the sandbox api
        """
        self.is_sandbox = sandbox
        self.api_request = ApiRequest(
            app_token=app_token,
            app_secret=app_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            is_sandbox=self.is_sandbox
        )

    def resolve(self, request_method, resource_url, params=None, data=None):
        """
        Resolve and send a request to the MKM endpoint.

        Can be used to send custom requests.

        :param request_method: GET, PUT, POST, DELETE, etc
        :param resource_url: URL that will be appended to the base endpoint URL
        :param params: A dictionary of query parameters for the request
        :param data: A dictionary that will be serialized to an MKM request object (see serializer class)
        :return: Returns the response received from the server
        """
        if isinstance(data, dict):
            serializer = XMLSerializer()
            data = serializer.serialize(data)

        if params is None:
            params = {}

        return self.api_request.request(url=resource_url, method=request_method, params=params, data=data)

    @property
    def account_management(self):
        return AccountManagement(self.resolve)

    @property
    def marketplace_info(self):
        return MarketplaceInfo(self.resolve)

    @property
    def order_management(self):
        return OrderManagement(self.resolve)

    @property
    def shopping_cart_manipulation(self):
        return ShoppingCartManipulation(self.resolve)

    @property
    def stock_management(self):
        return StockManagement(self.resolve)

    @property
    def wants_list_management(self):
        return WantsListManagement(self.resolve)
