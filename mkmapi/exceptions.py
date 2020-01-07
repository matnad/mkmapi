class MKMConnectionError(Exception):
    """Wraps errors related with requests to backend."""

    def __init__(self, response=None, message=None):
        """
        Initializes the exception with the response received from the backend.

        :param response: The response received from backend
        :param message: A custom message
        """

        self.response = response
        self.message = message

    def __str__(self):
        """Formats the error for the user so that it's easier to understand."""
        message = 'Request failed'
        if hasattr(self.response, 'status_code'):
            message = f'{message}\nStatus code: {self.response.status_code}'
        if hasattr(self.response, 'reason'):
            message = f'{message}\nResponse message: {self.response.reason}'
        if hasattr(self.response, 'content'):
            message = f'{message}\n{self.response.content}'
        if self.message:
            message = f'{message}\n{self.message}'
        return message


class MissingEnvVar(Exception):
    """Error for missing environment variables like auth credentials."""

    def __init__(self, env):
        """
        Initializes the exception with the missing variable name.

        :param env: The missing environment variable
        """
        self.env = env

    def __str__(self):
        return f'Missing environment variable `{self.env}`'


class SerializationException(Exception):
    """Error raised during XML serialization."""

    def __str__(self):
        return f'Serialization exception. {self.args}'
