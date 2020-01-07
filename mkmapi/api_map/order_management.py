import warnings


class OrderManagement:
    """
    Requests grouped to order management let you retrieve information about your orders,
    both where you're buyer or seller, as well as change their states (mark them as sent, received, etc.):
    """

    def __init__(self, resolve):
        self.resolve = resolve

    def get_order(self, order_id: int):
        """
        Returns an order specified by its ID.

        :param order_id: ID of the order (integer)
        :return: Response Object - Order
        """
        request_method = 'GET'
        resource_url = f'/order/{order_id}'

        return self.resolve(request_method, resource_url)

    def modify_order(self, order_id: int, action: str, reason: str = None, relist_items: bool = None):
        """
         Changes the state of an order specified by its ID.

        :param order_id: ID of the order (integer)
        :param action: Possible values for action:
            send - can be performed by the seller, if the current state is paid
            confirmReception - can be performed by the buyer, if the current state is sent
            cancel - can be performed by the seller, if the current state is bought for more than 7 days;
                can be performed by the buyer, if the current state is paid for more than 7 days
            requestCancellation - can be performed by both, if the state is not yet sent, the additional key
                reason is required; if the seller requests cancellation, an optional key relistItems can be
                provided to indicate, if the articles of the order should be relisted after the cancellation
                request was accepted by the buyer
            acceptCancellation - can be performed by both (but must be opposing actor), if the state is
                cancellationRequested; if the seller accepts the cancellation request, an optional key
                relistItems can be provided to indicate, if the articles of the order should be relisted thereafter
        :param reason: The reason for the cancellation request; only applicable, if action == requestCancellation
        :param relist_items: true|false, only applicable (and optional)
            if action == requestCancellation and the actor is the seller of the order, or
            if action == acceptCancellation and the actor is the seller of the order
        :return: Response Object - Order
        """
        request_method = 'PUT'
        resource_url = f'/order/{order_id}'

        possible_actions = ['send', 'confirmReception', 'cancel', 'requestCancellation', 'acceptCancellation']

        if not isinstance(action, str) or action not in possible_actions:
            warnings.warn(
                "action is potentially malformed. "
                f"Possible values: {', '.join(possible_actions)}.",
                SyntaxWarning
            )
        data = {'action': action}

        if action == 'requestCancellation' and isinstance(reason, str):
            data['reason'] = reason

        if action == 'requestCancellation' or action == 'acceptCancellation' and relist_items is not None:
            data['relistItems'] = 'true' if relist_items else 'false'

        return self.resolve(request_method, resource_url, data=data)

    def set_tracking_number(self, order_id: int, tracking_number: str):
        """
        Provides a tracking number to an order

        :param order_id: ID of the order (integer)
        :param tracking_number: Tracking number to add to the order (string)
        :return: Response Object - Order
        """
        request_method = 'PUT'
        resource_url = f'/order/{order_id}/tracking'
        data = {'trackingNumber': tracking_number}

        return self.resolve(request_method, resource_url, data=data)

    def evaluate_order(self, order_id: int, grade, item_description, packaging, comment, complaints):
        """
        Evaluates an order specified by its ID.

        :param order_id: ID of the order (integer)
        :param grade: 1 - very good; 2 - good; 3 - neutral; 4 - bad; 10 - n/a
        :param item_description: 1 - very good; 2 - good; 3 - neutral; 4 - bad; 10 - n/a
        :param packaging: 1 - very good; 2 - good; 3 - neutral; 4 - bad; 10 - n/a
        :param comment: Your comment for the order.
        :param complaints: A single complaint or a list/tuple of complaints. Pre-defined Strings.
        :return: Response Object - Order
        """
        request_method = 'POST'
        resource_url = f'/order/{order_id}/evaluation'
        data = {
            'evaluationGrade': grade,
            'itemDescription': item_description,
            'packaging': packaging,
            'comment': comment,
            'complaint': complaints
        }
        return self.resolve(request_method, resource_url, data=data)

    def filter_orders(self, actor, state, start: int = None):
        """
        Returns a collection of orders specified by the actor parameter (buyer or seller) and the state parameter
        (bought, paid, sent, received, lost, cancelled). Only orders for the authenticated user are returned.
        You can specify parameters for start and maximum results returned.
        If the response would have more than 1.000 entities a Temporary Redirect is returned.

        :param actor: seller or 1, buyer or 2
        :param state: bought or 1, paid or 2, sent or 4, received or 8, lost or 32, cancelled or 128
        :param start: If specified, only 100 entities are returned starting from the number provided
        :return: Response Object - Order
        """
        request_method = 'GET'
        resource_url = f'/orders/{actor}/{state}'
        if start is not None:
            resource_url += f'/{start}'
        return self.resolve(request_method, resource_url)
