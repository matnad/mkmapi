from oauthlib.oauth1 import Client


class MKMClient(Client):
    """
    A personalized OAuth1 Client used for Widget Applications.
    Original author: https://github.com/evonove
    """

    def get_oauth_params(self, request):
        """
        A modified version of the original method get_oauth_params,
        this version appends the `oauth_token` parameter as an empty
        string to the parameters list if not found in it.
        """

        parameters = super(MKMClient, self).get_oauth_params(request)

        oauth_param_exist = False
        # Loop through the parameters to check if oauth_token is found
        for param in parameters:
            if 'oauth_token' in param:
                oauth_param_exist = True
                break

        # We append the empty string oauth_token if it's not already there since MKM expects
        # the OAuth1 Header to have the parameter in any case, this has to be done otherwise
        # the response will always be 401 Unauthorized
        # Documentation: https://www.mkmapi.eu/ws/documentation/API:Auth_OAuthHeader
        if not oauth_param_exist:
            parameters.append((u'oauth_token', u''))

        return parameters
