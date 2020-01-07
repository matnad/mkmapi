class WantsListManagement:
    """
    Requests grouped to wants list management let you retrieve information about your stored wants lists,
    as well as let you manipulate them - creating new lists, add, edit, and delete wants lists and wants.
    """

    def __init__(self, resolve):
        self.resolve = resolve

    def get_wants_lists(self):
        """
        Returns a list with all of the user's wantslists, their name, associated game, and item count

        :return: Response Object - WantsList
        """
        request_method = 'GET'
        resource_url = '/wantslist'

        return self.resolve(request_method, resource_url)

    def create_wants_list(self, name: str, game_id: int = 1):
        """
        Creates a wantslist.

        :param name: Name of the list
        :param game_id: Game ID the list is for
        :return: Response Object - WantsList
        """
        request_method = 'POST'
        resource_url = '/wantslist'

        data = {
            'wantslist': [{'name': name, 'idGame': game_id}]
        }

        return self.resolve(request_method, resource_url, data=data)

    def get_wants_list(self, wants_list_id: int):
        """
        Returns the single specified wantslist with its details and items.

        :param wants_list_id: ID of the wants list
        :return: Response Object - WantsList, WantsListItem
        """
        request_method = 'GET'
        resource_url = f'/wantslist/{wants_list_id}'

        return self.resolve(request_method, resource_url)

    def rename_wants_list(self, wants_list_id: int, new_name: str):
        """
        Rename a wants list.

        :param wants_list_id: ID of the wants list to rename
        :param new_name: New name for the wants list
        :return: Response Object - WantsList, WantsListItem
        """
        request_method = 'PUT'
        resource_url = f'/wantslist/{wants_list_id}'

        data = {
            'action': 'editWantslist',
            'name': new_name
        }

        return self.resolve(request_method, resource_url, data=data)

    def delete_wants_list(self, wants_list_id: int):
        """
        Delete a wants list and all its items.

        :param wants_list_id: ID of the wants list to delete
        :return: Response Object - WantsList, WantsListItem
        """
        request_method = 'DELETE'
        resource_url = f'/wantslist/{wants_list_id}'

        data = {
            'action': 'deleteWantslist',
        }

        return self.resolve(request_method, resource_url, data=data)

    def bulk_edit_wants_list(self, wants_list_id: int, action: str, category: str, items):
        """
        Add, edit or delete items on a specified wants list.

        See https://api.cardmarket.com/ws/documentation/API_2.0:Wantslist_Item for more details.

        :param wants_list_id: ID of the wants list
        :param action: addItem, editItem or deleteItem
        :param category: product, metaproduct or want (an item already on the list)
        :param items: List/Tuple of items with variable parameters. See documentation.
            Example for addItem with category product:
            [{'idProduct': 1234545, 'count': 1, 'minCondition': 'PL', 'wishPrice': 10, 'mailAlert': 'false'}]
        :return: Response Object - WantsList, WantsListItem
        """
        request_method = 'PUT'
        resource_url = f'/wantslist/{wants_list_id}'

        if not isinstance(items, (list, tuple)):
            items = [items]

        data = {
            'action': action,
            category: items
        }

        return self.resolve(request_method, resource_url, data=data)
