import warnings


class MarketplaceInfo:
    """
    All Market Place request give you information about things from MKM's market place - games we support,
    products we list, articles available at the market, or user registered at MKM.
    """

    def __init__(self, resolve):
        self.resolve = resolve

    def get_games(self):
        """
        Returns all games supported by MKM and you can sell and buy products for.

        :return: Response Object - Game
        """
        request_method = 'GET'
        resource_url = '/games'
        return self.resolve(request_method, resource_url)

    def get_expansion(self, game_id: int):
        """
        Returns all expansions with single cards for the specified game.

        :param game_id: ID of the game, see get_games()
        :return: Response Object - Expansion
        """
        request_method = 'GET'
        resource_url = f'/games/{game_id}/expansions'
        return self.resolve(request_method, resource_url)

    def get_expansion_singles(self, expansion_id: int):
        """
        Returns all single cards for the specified expansion.

        :param expansion_id: ID of the expansion, see get_expansion()
        :return: Response Object - Expansion, Product (without details)
        """
        request_method = 'GET'
        resource_url = f'/expansions/{expansion_id}/singles'
        return self.resolve(request_method, resource_url)

    def get_product(self, product_id: int):
        """
        Returns a product specified by its ID.

        :param product_id: ID of the product
        :return: Response Object - Product (detailed)
        """
        request_method = 'GET'
        resource_url = f'/products/{product_id}'
        return self.resolve(request_method, resource_url)

    def get_product_list(self):
        """
        Returns a gzipped CSV file with all relevant products available at Cardmarket.
        The response object and the relevant productsfile contains a string which is Base64 encoded.
        Decoding it returns a binary string that has to be written to an empty file.
        This file is gzipped and finally needs to be unpacked to retrieve the CSV file.

        :return: Base64 encoded string. See above.
        """
        request_method = 'GET'
        resource_url = '/productlist'
        return self.resolve(request_method, resource_url)

    def get_price_guide(self, game_id: int = 1):
        """
        Attention: This request is restricted to Widget apps, 3rd party apps, and Dedicated apps of
        powersellers and professionals.

        Returns a gzipped CSV file with relevant price guides for the specified game (default: MtG).

        The file is updated once every two hours.
        Security mechanisms will be implemented to return a 427 if requested more frequently.

        The response object and the relevant priceguidefile contains a string which is Base64 encoded.
        Decoding it returns a binary string that has to be written to an empty file.
        This file is gzipped and finally needs to be unpacked to retrieve the CSV file.

        :param game_id: ID of the game (default: 1 for MtG)
        :return: Base64 encoded string. See above.
        """
        request_method = 'GET'
        resource_url = '/priceguide'
        if isinstance(game_id, int) and game_id > 1:
            params = {'idGame': game_id}
        else:
            params = {}
        return self.resolve(request_method, resource_url, params=params)

    def find_products(
            self, query: str, is_exact: bool = True, game_id: int = 1, language_id: int = 1,
            start: int = None, max_results: int = None
    ):
        """
        Searches for products by a given search string.

        start and max_results are ignored unless both are specified.

        :param query: search string
        :param is_exact: Flag that indicates if only products should be returned where the name
            exactly matches the search string (default: True)
        :param game_id: ID of the game (default: 1 for MtG)
        :param language_id: ID of the language (default: 1 for English)
        :param start: If specified, the first (start - 1) results are skipped
        :param max_results: If specified, at most max_results entries are returned
        :return: Response Object - Product (without details)
        """
        request_method = 'GET'
        resource_url = '/products/find'
        params = {
            'search': query,
            'exact': 'true' if is_exact else 'false',
            'idGame': game_id,
            'idLanguage': language_id,
        }
        if isinstance(start, int) and isinstance(max_results, int):
            params['start'] = start
            params['maxResults'] = max_results

        return self.resolve(request_method, resource_url, params=params)

    def get_articles_for_product(
            self, product_id: int, start: int = None, max_results: int = None, user_type: str = None,
            min_user_score: int = None, language_id: int = None, min_condition: str = None,
            is_foil: bool = None, is_signed: bool = None, is_altered: bool = None,
            min_available: int = None
    ):
        """
        Returns all available articles for a specified product.

        If the response would have more than 1.000 entities a Temporary Redirect is returned.
        You can specify several filter parameters.

        start and max_results are ignored unless both are specified.

        :param product_id: ID of the product (integer, required)
        :param start: If specified, the first (start - 1) results are skipped
        :param max_results: If specified, at most max_results entries are returned
        :param user_type: only articles from sellers with the specified user type are returned
            (private for private sellers only;
            commercial for all commercial sellers, including powersellers;
            powerseller for powersellers only)
        :param min_user_score: only articles from sellers with the sepcified user score or better are returned
            (1 for outstanding > 2 for very good > 3 good > 4 for average > 5 for bad)
        :param language_id: only articles are returned that match the give language
            (1 for English; 2 for French; 3 for German; 4 for Spanish; 5 for Italian; 6 for Simplified Chinese;
            7 for Japanese; 8 for Portuguese; 9 for Russian; 10 for Korean; 11 for Traditional Chinese)
        :param min_condition: only articles with the specified condition or better are returned
            (MT for Mint > NM for Near Mint > EX for Exellent > GD for Good > LP for Light Played
            > PL for Played > PO for Poor)
        :param is_foil: True/False - Only/No articles that are flagged as foil are returned.
            Omitting this returns both.
        :param is_signed: True/False - Only/No articles that are flagged as signed are returned.
            Omitting this returns both.
        :param is_altered: True/False - Only/No articles that are flagged as altered are returned.
            Omitting this returns both.
        :param min_available: only articles with a minimum amount as specified are returned.
            Attention: The minimum amount refers to the total number of copies from that seller.
            If you search for minAvailable=4, you will also get results with count lower than 4 if that seller has
            additional copies for a different price, condition, etc. but always matching all of your search criteria.
        :return: Response Object - Article
        """
        request_method = 'GET'
        resource_url = f'/articles/{product_id}'
        params = {'idProduct': product_id}

        if isinstance(start, int) and isinstance(max_results, int):
            params['start'] = start
            params['maxResults'] = max_results

        if user_type is not None:
            if not isinstance(user_type, str) or user_type not in ['private', 'commercial', 'powerseller']:
                warnings.warn(
                    "user_type is potentially malformed. "
                    "'private' for private sellers only; 'commercial' for all commercial sellers, "
                    "including powersellers; 'powerseller' for powersellers only",
                    SyntaxWarning
                )
            params['userType'] = user_type

        if min_user_score is not None:
            if not isinstance(min_user_score, int) or min_user_score < 1 or min_user_score > 5:
                warnings.warn(
                    "min_user_score is potentially malformed. "
                    "1 for outstanding > 2 for very good > 3 good > 4 for average > 5 for bad",
                    SyntaxWarning
                )
            params['minUserScore'] = min_user_score

        if language_id is not None:
            if not isinstance(language_id, int) or language_id < 1 or language_id > 11:
                warnings.warn(
                    "language_id is potentially malformed. "
                    "1 for English; 2 for French; 3 for German; 4 for Spanish; 5 for Italian; "
                    "6 for Simplified Chinese; 7 for Japanese; 8 for Portuguese; 9 for Russian; "
                    "10 for Korean; 11 for Traditional Chinese",
                    SyntaxWarning
                )
            params['idLanguage'] = language_id

        if min_condition is not None:
            if not isinstance(min_condition, str) or min_condition not in ['MT', 'NM', 'EX', 'GD', 'LP', 'PL', 'PO']:
                warnings.warn(
                    "min_condition is potentially malformed. Make sure the condition label is in ALL CAPS."
                    "MT for Mint > NM for Near Mint > EX for Exellent > GD for Good > LP for Light Played "
                    "> PL for Played > PO for Poor",
                    SyntaxWarning
                )
            params['minCondition'] = min_condition

        if is_foil is not None:
            params['isFoil'] = 'true' if is_foil else 'false'
        if is_signed is not None:
            params['isSigned'] = 'true' if is_signed else 'false'
        if is_altered is not None:
            params['isAltered'] = 'true' if is_altered else 'false'

        if min_available is not None:
            if not isinstance(min_available, int) or min_available < 0:
                warnings.warn(
                    "min_available is potentially malformed. Make sure it is an integer equal to or greater than 0.",
                    SyntaxWarning
                )
            params['minAvailable'] = min_available

        return self.resolve(request_method, resource_url, params=params)

    def get_metaproduct(self, metaproduct_id):
        """
        Returns the metaproduct specified by its ID.

        :param metaproduct_id: ID of the metaproduct
        :return: Response Object - Metaproduct
        """
        request_method = 'GET'
        resource_url = f'/metaproducts/{metaproduct_id}'
        return self.resolve(request_method, resource_url)

    def find_metaproducts(self, query: str, is_exact: bool = True, game_id: int = 1, language_id: int = 1):
        """
        Searches for metaproducts by a given search string.

        :param query: search string
        :param is_exact: Flag that indicates if only products should be returned where the name
            exactly matches the search string (default: True)
        :param game_id: ID of the game (default: 1 for MtG)
        :param language_id: ID of the language (default: 1 for English)
        :return: Response Object - Metaproduct
        """
        request_method = 'GET'
        resource_url = '/metaproducts/find'
        params = {
            'search': query,
            'exact': 'true' if is_exact else 'false',
            'idGame': game_id,
            'idLanguage': language_id,
        }

        return self.resolve(request_method, resource_url, params=params)

    def get_user(self, user_id):
        """
        Returns the user specified either by its ID, or its exact name.

        :param user_id: User ID or exact username
        :return: Response Object - User
        """
        request_method = 'GET'
        resource_url = f'/users/{user_id}'

        return self.resolve(request_method, resource_url)

    def find_users(self, query: str):
        """
        Returns users where the username is matching the given search string.
        The given search string must be at least 3 characters long.

        A maximum of 50 users is returned.

        :param query: String matching the username
        :return: Response Object - User
        """
        request_method = 'GET'
        resource_url = '/users/find'
        params = {'search': query}

        return self.resolve(request_method, resource_url, params=params)

    def get_articles_for_user(self, user_id, game_id: int = 1, start: int = None, max_results: int = None):
        """
        Returns the available articles for a specified user.

        The response can be paginated by using the start and maxResults parameters.
        start and max_results are ignored unless both are specified.

        :param user_id: User ID or Username
        :param game_id: ID of the game (default: 1 for MtG)
        :param start: If specified, the first (start - 1) results are skipped
        :param max_results: If specified, at most max_results entries are returned
        :return: Response Object - Article
        """
        request_method = 'GET'
        resource_url = f'/users/{user_id}/articles'
        params = {
            'idUser': user_id,
            'idGame': game_id,
        }
        if isinstance(start, int) and isinstance(max_results, int):
            params['start'] = start
            params['maxResults'] = max_results

        return self.resolve(request_method, resource_url, params=params)
