import warnings


class ShoppingCartManipulation:
    """
    Requests grouped to order management let you retrieve information about your orders, both where you're
    buyer or seller, as well as change their states (mark them as sent, received, etc.).
    """

    def __init__(self, resolve):
        self.resolve = resolve

    def get_shopping_cart(self):
        """
        Returns the shopping cart entity for the authenticated user.

        :return: Response Object - Shopping Cart
        """
        request_method = 'GET'
        resource_url = '/shoppingcart'

        return self.resolve(request_method, resource_url)

    def bulk_edit_shopping_cart(self, action, articles):
        """
        Add or remove multiple articles to or from the shopping cart.

        To add/remove a single article, you can use the more convenient methods add/remove_to_shopping_cart()

        :param action: add or remove
        :param articles: A list/turple of dictionaries with entries for idArticle and amount or count like:
            [{'idArticle': 1234, 'amount': 1}, {'idArticle': 3456, 'count': 2}]
        :return: Response Object - Shopping Cart
        """
        request_method = 'PUT'
        resource_url = '/shoppingcart'
        if not isinstance(articles, (list, tuple)):
            articles = [articles]
        if action not in ['add', 'remove']:
            warnings.warn(
                "action is potentially malformed. "
                f"Possible values: add, remove.",
                SyntaxWarning
            )
        data = {
            'action': action,
            'article': articles
        }

        return self.resolve(request_method, resource_url, data=data)

    def add_to_shopping_cart(self, article_id, amount: int = None):
        """
        Add a specified quantity of a single item to the shopping cart.

        :param article_id: ID of the article to add
        :param amount: specify the amount you want to add
        :return: Response Object - Shopping Cart
        """
        return self.bulk_edit_shopping_cart("add", {'idArticle': article_id, 'amount': amount})

    def remove_from_shopping_cart(self, article_id, amount: int = None):
        """
        Remove a specified quantity of a single item from the shopping cart.

        :param article_id: ID of the article to add
        :param amount: specify the amount you want to add
        :return:
        """
        return self.bulk_edit_shopping_cart("remove", {'idArticle': article_id, 'amount': amount})

    def empty_shopping_cart(self):
        """
        Empties the authenticated user's shopping cart.

        :return: Response Object - Shopping Cart
        """
        request_method = 'DELETE'
        resource_url = '/shoppingcart'

        return self.resolve(request_method, resource_url)

    def checkout_and_pay(self):
        """
        Checks out the authenticated user's shopping cart and creates the respective orders.
        The most orders possible will be paid from the user's account balance.

        :return: Response Object - Order
        """
        request_method = 'PUT'
        resource_url = '/shoppingcart/checkout'

        return self.resolve(request_method, resource_url)

    def change_shipping_address(self, name, street, zipcode, city, country, extra=None):
        """
        Changes the authenticated user's shipping address for all reservations in the shopping cart.
        This address becomes active and will be attached to the created orders after the checkout.

        :param name: Full name
        :param street: Street name and number
        :param zipcode: Zip code of city
        :param city: Name of city
        :param country: Country code or name
        :param extra: Title, c/o, etc (optional)
        :return: Response Object - Shopping Cart
        """
        request_method = 'PUT'
        resource_url = '/shoppingcart/shippingaddress'

        data = {
            'name': name,
            'extra': extra if extra is not None else '',
            'street': street,
            'zip': zipcode,
            'city': city,
            'country': country
        }

        return self.resolve(request_method, resource_url, data=data)

    def get_shipping_methods(self, reservation_id):
        """
        Returns the all possible shipping method entities for the specified reservation within the
        authenticated user's shopping cart.

        :param reservation_id: ID of the reservation
        :return: Response Object - Shipping Method
        """
        request_method = 'GET'
        resource_url = f'/shoppingcart/shippingmethod/{reservation_id}'

        return self.resolve(request_method, resource_url)

    def change_shipping_method(self, reservation_id, shipping_method_id):
        """
        Changes the shipping method of a specified reservation in the authenticated user's shopping cart.
        Use get_shipping_methods() to get a list of valid shipping_method_ids.

        :param reservation_id:
        :param shipping_method_id:
        :return: Response Object - Shopping Cart
        """
        request_method = 'PUT'
        resource_url = f'/shoppingcart/shippingmethod/{reservation_id}'

        data = {'idShippingMethod': shipping_method_id}

        return self.resolve(request_method, resource_url, data=data)
