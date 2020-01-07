# Magic CardMarket (MKM) API Library

A full wrapper for the [MKM API 2.0](https://api.cardmarket.com/ws/documentation/API_2.0:Main_Page)

# Requirements
* Python 3.4+
* oauthlib
* Requests
* Requests_OAuthlib

# Setup

```
pip install mkmapi
```

Make sure the requirements are installed (see requirements.txt)

# Usage
Find your credentials in your MKM account under the apps section.
You can store them as environment variables or pass them to the constructor (as show below).

Import the Mkm class and instantiate it.

```python
from mkmapi.mkm import Mkm

mkm = Mkm(
    app_token='asdf123',
    app_secret='secret456',
    access_token='ghjkl789',
    access_token_secret='0112yxcv'
)
```

Make a request.

```python
response = mkm.account_management.get_account_information()
```

Print the response
```python
import json 

json_response = json.loads(response.content)
print(json.dumps(json_response, indent=2))
```

# Features
* Full support with docstrings and autocomplete for modern IDEs.
* Most methods have a full interface with named parameters.
* It's possible to send raw queries via `mkm.resolve(method, url, params, **kwargs)`.

# Credit
Thanks to https://github.com/evonove/ for his work on the serialization and OAuth