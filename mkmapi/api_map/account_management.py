class AccountManagement:
    """
    All Account requests allow managing the authenticated user's account or are in some way
    connected to account management.
    """

    def __init__(self, resolve):
        self.resolve = resolve

    def get_account_information(self):
        """
        Returns the account details of the authenticated user.

        :return: Response Object - Account
        """
        request_method = 'GET'
        resource_url = '/account'
        return self.resolve(request_method, resource_url)

    def change_vacation_status(self, on_vacation: bool, cancel_orders: bool = False, relist_items: bool = False):
        """
        Updates the vacation status of the user.

        :param on_vacation: Boolean flag if the user is on vacation or not
        :param cancel_orders: Boolean flag to cancel open orders, resp. request cancellation for open orders
        :param relist_items: Boolean flag to relist items for canceled orders;
            only applies if cancelOrders is also provided and set to true for all orders, that are effectively canceled
        :return: Response Object - Account
        """
        request_method = 'PUT'
        resource_url = f'/account/vacation'
        params = {
            'onVacation': 'true' if on_vacation else 'false',
            'cancelOrders': 'true' if cancel_orders else 'false',
            'relistItems': 'true' if relist_items else 'false'
        }
        return self.resolve(request_method, resource_url, params=params)

    def change_display_language(self, new_language: int):
        """
        Updates the display language of the authenticated user.

        :param new_language: 1: English, 2: French, 3: German, 4: Spanish, 5: English
        :return: Response Object - Account
        """
        if not isinstance(new_language, int) or new_language < 1 or new_language > 5:
            raise ValueError('The new language must be a number between 1 and 5.')
        request_method = 'PUT'
        resource_url = '/account/language'
        params = {'idDisplayLanguage': new_language}
        return self.resolve(request_method, resource_url, params=params)

    def get_message_overview(self):
        """
        Returns the message thread overview of the authenticated user.

        :return: Response Object - Message Thread
        """
        request_method = 'GET'
        resource_url = '/account/messages'
        return self.resolve(request_method, resource_url)

    def get_messages_from(self, other_user_id: int):
        """
        Returns the message thread with a specified other user.

        :param other_user_id: ID of the other user (as integer)
        :return: Response Object - Message Thread
        """
        if not isinstance(other_user_id, int):
            raise ValueError('The user id must be an integer.')
        request_method = 'GET'
        resource_url = f'/account/messages/{other_user_id}'
        return self.resolve(request_method, resource_url)

    def get_message_from(self, other_user_id: int, message_id: str):
        """
        Returns a specified message with a specified other user.

        :param other_user_id: ID of the other user (as integer)
        :param message_id: ID of the message (as string)
        :return: Response Object - Message Thread
        """
        if not isinstance(other_user_id, int):
            raise ValueError('The user id must be an integer.')
        if not isinstance(message_id, str):
            raise ValueError('The message id must be a (hex) string.')
        request_method = 'GET'
        resource_url = f'/account/messages/{other_user_id}/{message_id}'
        return self.resolve(request_method, resource_url)

    def send_message(self, other_user_id: int, message: str):
        """
        Creates a new message sent to a specified other user.

        :param other_user_id: ID of the other user (as integer)
        :param message: Text of the message to send. Use '\n' for newline.
        :return: Response Object - Message Thread (With only the message just sent)
        """
        if not isinstance(other_user_id, int):
            raise ValueError('The user id must be an integer.')
        request_method = 'POST'
        resource_url = f'/account/messages/{other_user_id}'
        data = {'message': message}
        return self.resolve(request_method, resource_url, data=data)

    def delete_message(self, other_user_id: int, message_id: str):
        """
        Deletes a specified message to a specified other user.
        The message will be delete just for you, it is still visible to the other user.

        :param other_user_id: ID of the other user (as integer)
        :param message_id: ID of the message (as string)
        :return: Empty
        """
        if not isinstance(other_user_id, int):
            raise ValueError('The user id must be an integer.')
        if not isinstance(message_id, str):
            raise ValueError('The message id must be a (hex) string.')
        request_method = 'DELETE'
        resource_url = f'/account/messages/{other_user_id}/{message_id}'
        return self.resolve(request_method, resource_url)

    def delete_messages_from(self, other_user_id: int):
        """
        Deletes a complete message thread to a specified other user.

        :param other_user_id: ID of the other user (as integer)
        :return: Empty
        """
        if not isinstance(other_user_id, int):
            raise ValueError('The user id must be an integer.')
        request_method = 'DELETE'
        resource_url = f'/account/messages/{other_user_id}'
        return self.resolve(request_method, resource_url)

    def get_unread_messages(self):
        """
        Returns all unread messages.
        This request returns only messages where the authenticated user is the receiver.

        Note: As of Jan 2020 there is a confirmed issue with this method on the MKM backend resulting in a
        Bad Request (400) status code for some users.

        :return: Response Object - Message
        """
        request_method = 'GET'
        resource_url = '/account/messages/find'
        params = {'unread': 'true'}
        return self.resolve(request_method, resource_url, params=params)

    def get_messages_between(self, start_date: str, end_date: str = None):
        """
        Returns all messages between the start and end date.
        If the end date is omitted, the current date is assumed.
        The safest format to use is the ISO 8601 representation:

        E.g. 2017-12-08T14:41:12+0100 (YYYY-MM-DDTHH:MM:SS+HHMM) for 8th of December, 2017, 14:41:12 CET
        Be aware that the colon (:) in time representations is a reserved character and needs to be percent encoded.

        Note: As of Jan 2020 there is a confirmed issue with this method on the MKM backend resulting in a
        Bad Request (400) status code for some users.

        :param start_date: The earliest date to get messages
        :param end_date: The lastest date to get messages (current date if omitted)
        :return: Response Object - Message
        """
        request_method = 'GET'
        resource_url = '/account/messages/find'
        params = {'startDate': start_date}
        if end_date is not None:
            params['endDate'] = end_date
        return self.resolve(request_method, resource_url, params=params)

    def redeem_coupon(self, coupon_code):
        """
        Redeems one coupon.

        :param coupon_code: Code of the coupon to redeem
        :return: Response Object - Account plus CodeRedemption
        """
        request_method = 'POST'
        resource_url = f'/account/coupon'
        data = {'couponCode': coupon_code}
        return self.resolve(request_method, resource_url, data=data)
