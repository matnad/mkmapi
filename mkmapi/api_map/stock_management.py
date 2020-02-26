import warnings


class StockManagement:
    """
    Requests grouped to stock management let you retrieve information about the articles you want to sell,
    as well as put new articles into the stock, remove them from, or edit them.
    """

    def __init__(self, resolve):
        self.resolve = resolve

    def get_stock(self, start: int = None):
        """
        Returns the Article entities in the authenticated user's stock.

        :param start: If specified, only 100 entities are returned starting from the number provided
        :return: Response Object - Article
        """
        request_method = 'GET'
        resource_url = '/stock'

        params = {}
        if isinstance(start, int):
            params['start'] = start

        return self.resolve(request_method, resource_url, params=params)

    def bulk_modify_stock(self, action, articles):
        """
        Add, change or remove a list of articles in your stock.

        :param action: add, change or remove
        :param articles: list/tuple of dicts with the desired attributes.
            See: https://api.cardmarket.com/ws/documentation/API_2.0:Stock
        :return: Response Object - Article
        """
        if action == 'add':
            request_method = 'POST'
        elif action == 'change':
            request_method = 'PUT'
        elif action == 'remove':
            request_method = 'DELETE'
        else:
            warnings.warn("Actions must be add, change or remove.", SyntaxWarning)
            return None

        resource_url = '/stock'
        if not isinstance(articles, (list, tuple)):
            articles = [articles]

        data = {'article': articles}

        return self.resolve(request_method, resource_url, data=data)

    def add_product_to_stock(
            self, product_id: int, amount: int, language_id: int, price: float, comments: str = "",
            condition: None = str, is_foil: bool = False, is_signed: bool = False, is_altered: bool = False,
            is_playset: bool = False, is_first_ed: bool = False
    ):
        """
        Adds new articles to the user's stock.

        :param product_id: ID of product
        :param amount: Amount of stock to add
        :param language_id: Language code
        :param comments: Comment for the article
        :param price: Price of the article in EUR
        :param condition: Condition if applicable (optional)
        :param is_foil: True if card is foil (default: False)
        :param is_signed: True if card is signed (default: False)
        :param is_altered: True if card is altered (default: False)
        :param is_playset: True if article is a playset (4 cards) (default: False)
        :param is_first_ed: True if card is from the First Edition (default: False)
        :return: Response Object - Article
        """
        article = {
            'idProduct': product_id,
            'count': amount,
            'idLanguage': language_id,
            'comments': comments,
            'price': price,
            'isFoil': 'true' if is_foil else 'false',
            'isSigned': 'true' if is_signed else 'false',
            'isAltered': 'true' if is_altered else 'false',
            'isPlayset': 'true' if is_playset else 'false',
            'isFirstEd': 'true' if is_first_ed else 'false'
        }

        if condition is not None:
            article['condition'] = condition

        return self.bulk_modify_stock("add", article)

    def change_product_in_stock(
            self, article_id: int, amount_to_edit: int, language_id: int, price: float, comments: str = "",
            condition: None = str, is_foil: bool = False, is_signed: bool = False, is_altered: bool = False,
            is_playset: bool = False, is_first_ed: bool = False
    ):
        """
        Changes an article in the user's stock.
        You need to specify ALL the properties, otherwise they will be replaced by default values.

        :param article_id: ID of article to change
        :param amount_to_edit: Amount of stock to edit.
            NOT the new quantity! This has to be changed with a dedicated method
        :param language_id: Language code
        :param comments: Comment for the article
        :param price: Price of the article in EUR
        :param condition: Condition if applicable (optional)
        :param is_foil: True if card is foil (default: False)
        :param is_signed: True if card is signed (default: False)
        :param is_altered: True if card is altered (default: False)
        :param is_playset: True if article is a playset (4 cards) (default: False)
        :param is_first_ed: True if card is from the First Edition (YuGiOh only) (default: False)
        :return: Response Object - Article
        """
        article = {
            'idArticle': article_id,
            'count': amount_to_edit,
            'idLanguage': language_id,
            'comments': comments,
            'price': price,
            'isFoil': 'true' if is_foil else 'false',
            'isSigned': 'true' if is_signed else 'false',
            'isAltered': 'true' if is_altered else 'false',
            'isPlayset': 'true' if is_playset else 'false',
            'isFirstEd': 'true' if is_first_ed else 'false'
        }

        if condition is not None:
            article['condition'] = condition

        return self.bulk_modify_stock("change", article)

    def remove_article_from_stock(self, article_id, amount_to_delete):
        """
        Deletes an article from the stock.

        :param article_id: ID of article to change
        :param amount_to_delete: Amount of stock to delete
        :return: Response Object - Article
        """
        article = {
            'idArticle': article_id,
            'count': amount_to_delete,
        }
        return self.bulk_modify_stock("remove", article)

    def get_stock_as_file(self, game_id: int = 1, is_sealed: bool = False, language_id: int = 1):
        """
        Returns a gzipped CSV file with all articles in the authenticated user's stock,
        further specified by a game, language, and type of articles (single cards or sealed products).

        The response object and the relevant stock contains a string which is Base64 encoded.
        Decoding it returns a binary string that has to be written to an empty file.
        This file is gzipped and finally needs to be unpacked to retrieve the CSV file.

        :param game_id: Specifies the Game the stock file is for (optional; default: 1 (MtG))
        :param is_sealed: Specifies if sealed product should be returned (optional; default: false (singles))
        :param language_id: Specifies the Language of the Local Name column in the resulting file
            (optional; default: 1 (english))
        :return: Base64 encoded string. See above.
        """
        request_method = 'GET'
        resource_url = '/stock/file'
        params = {}
        if isinstance(game_id, int) and game_id > 1:
            params.update({'idGame': game_id})

        if isinstance(is_sealed, bool) and is_sealed == True:
            params.update({'isSealed': is_sealed})

        if isinstance(language_id, int) and language_id > 1:
            params.update({'idLanguage': language_id})

        return self.resolve(request_method, resource_url, params=params)

    def get_stock_in_shopping_carts(self):
        """
        Returns the Article entities of the authenticated user's stock that are currently in other user's shopping carts.

        :return: Response Object - Article
        """
        request_method = 'GET'
        resource_url = '/stock/shoppingcart-articles'

        return self.resolve(request_method, resource_url)

    def get_stock_article(self, article_id):
        """
        Returns a single article in the authenticated user's stock specified by its article ID.

        :param article_id: ID of the article
        :return: Response Object - Article
        """
        request_method = 'GET'
        resource_url = f'/stock/article/{article_id}'

        return self.resolve(request_method, resource_url)

    def find_stock_articles(self, name, game_id: int = 1):
        """
        Searches for and returns articles specified by the article's name and game.

        name should be provided in English, as that request is not reliably working with localized names at the moment.

        To retrieve accessories not specifically assigned to a game, you can provide game_id = 0.

        :param name: Search string for the product's name
        :param game_id: ID of related game or 0 if unrelated to a game
        :return: Response Object - Article
        """
        request_method = 'GET'
        resource_url = f'/stock/articles/{name}/{game_id}'

        return self.resolve(request_method, resource_url)

    def bulk_change_stock_quantity(self, increase_or_decrease, articles):
        """
        Changes quantities for articles in authenticated user's stock.

        Attention: Increasing the stock for an article may fail, because we have limitations on how many copies
        of an article different seller types (private, professional) can have in their stock. In this case, the
        response body will have the failed key collecting all articles that failed in increasing the copies -
        in addition to the article key collecting all successful increases.

        :param increase_or_decrease: 'increase' or 'decrease'
        :param articles: A list/turple of dictionaries with entries for idArticle and count like:
            [{'idArticle': 1234567, 'count': 1}]
        :return: Response Object - Article
        """
        request_method = 'PUT'
        resource_url = f'/stock/'

        if increase_or_decrease in ['increase', 'decrease']:
            resource_url += increase_or_decrease
        else:
            warnings.warn("increase_or_decrease must be 'increase' or 'decrease'.", SyntaxWarning)
            return None

        if not isinstance(articles, (list, tuple)):
            articles = [articles]

        data = {'article': articles}

        return self.resolve(request_method, resource_url, data=data)

    def increase_quantity_for_article(self, article_id: int, increase_by: int):
        """
        Increase quantity for an article in the authenticated user's stock.

        :param article_id: Article ID to increase stock for
        :param increase_by: Stock will be increased by this amount
        :return: Response Object - Article
        """
        return self.bulk_change_stock_quantity('increase', {'idArticle': article_id, 'count': increase_by})

    def decrease_quantity_for_article(self, article_id: int, decrease_by: int):
        """
        Decrease quantity for an article in the authenticated user's stock.

        :param article_id: Article ID to decrease stock for
        :param decrease_by: Stock will be decreased by this amount
        :return: Response Object - Article
        """
        return self.bulk_change_stock_quantity('decrease', {'idArticle': article_id, 'count': decrease_by})
