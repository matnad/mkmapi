from io import StringIO
from xml.sax.saxutils import XMLGenerator

from mkmapi.exceptions import SerializationException


class XMLSerializer:
    """
    Serializes data to XML for MKM requests.
    Original author: https://github.com/evonove
    """

    def __init__(self):
        self.generator = None

    def serialize(self, data):
        """
        Serializes data to XML so that it can be sent to backend, if data is not a dictionary.

        :raise SerializationException: On serialize error.
        :param data: A dictionary containing the data to serialize
        :return: Returns a string containing data serialized to XML
        """

        if not isinstance(data, dict):
            raise SerializationException("Can't serialize data, must be a dictionary.")

        stream = StringIO()
        self.generator = XMLGenerator(stream, 'utf-8')

        self.generator.startDocument()
        self.generator.startElement('request', {})

        self._parse(data)

        self.generator.endElement('request')
        self.generator.endDocument()

        return stream.getvalue()

    def _parse(self, data, previous_element_tag=None):
        """
        Recursively parses data and creates the relative elements.

        :param data: Data to parse
        :param previous_element_tag: When parsing a list we pass the previous element tag
        :return:
        """
        if isinstance(data, dict):
            for key in data:
                value = data[key]
                self._parse(value, key)

        elif isinstance(data, (list, tuple)):
            for item in data:
                if isinstance(item, dict):
                    self.generator.startElement(previous_element_tag, {})
                self._parse(item, previous_element_tag)
                if isinstance(item, dict):
                    self.generator.endElement(previous_element_tag)

        else:
            self.generator.startElement(previous_element_tag, {})
            self.generator.characters(f'{data}')
            self.generator.endElement(previous_element_tag)
