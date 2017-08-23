import requests

from lxml import html

from errors import ArgumentError
from utils import HTMLUtils, URLUtils


class HTMLPage(object):
    """Represents a full web/HTML page

    Attributes:
        link (Link): The link object that was used to create this
            HTMLPage instance
        status_code (int): HTTP status code for the current page
        encoding (str): The character encoding of the current page
        html_content (unicode): HTML content of the current page
        text_content (unicode): Text content (no HTML tags or script or styles)
            of the current page
        child_links (list): A list of Link object corresponding to all unique
            links present in the current page
    """
    def __init__(self, link):
        """Instantiates a HTMLPage object

        Args:
            link (Link): A valid Link object

        Raises:
            ArgumentError: If the arguments are faulty
        """
        # validate args
        if not isinstance(link, Link) or not link.is_valid:
            raise ArgumentError('HTMLPage class should be instantiated with ' \
                'a valid Link object. Got this: %s' %link)
        self.link = link

        # fetch the actual webpage
        response = requests.get(link.url)
        self.status_code = response.status_code
        self.html_content = response.text.encode('utf8')
        self.text_content = HTMLUtils.html_to_text(self.html_content)
        self.encoding = response.encoding

        # fetch all child links
        self.child_links = self._get_all_links()

    def get_links(self, allowed_domains=[]):
        """From the current HTML page, fetches all unique links inside a given
        list of allowed domains.

        Args:
            allowed_domains (list(str), optional): A list of allowed domains

        Returns:
            list(str): A list of unique Link objects
        """
        return [ link for link in self.child_links  \
            if link.domain in allowed_domains ]

    def has_word(self, word):
        """Checks the current HTML page for the presence of a given word

        The search is performed on the text content of the current page
        (excluding HTML tags, script sections, style sheet sections and
        invalid tags)

        Args:
            word (str): A non empty stop word

        Returns:
            bool: True, if the given word is present in the page; else False

        Raises:
            ArgumentError: If the arguments are faulty
        """
        # validate args
        if not word:
            raise ArgumentError('Param "word" cannot be empty')
        return word in self.text_content

    def _get_all_links(self):
        tree = html.fromstring(self.html_content)
        urls = set([ URLUtils.normalize(url) for url \
            in tree.xpath('//a[@href]/@href') ])
        return [ Link(url, self.link) for url in urls ]

    def __str__(self):
        return '[HTML PAGE] [LEVEL %s] %s ; ' \
            'HTTP STATUS:%s ; TOTAL CHILD_LINKS: %s' \
            %(self.link.level, self.link.url,
                self.status_code, len(self.child_links))


class Link(object):
    """Represents a URL, with a reference to the parent page's URL

    Attributes:
        parent (Link): The parent Link object which was used to create this
            child instance
        url (str): Normalized version of the URL (fragments removed)
        domain (str): Domain of the current URL
        is_valid (bool): True if the URL is properly structured; else False
        id (str): A 32-character string uniquely representing this URL/Link
        level (int): The level of the current URL (1 greater than its parent)
    """
    def __init__(self, url, parent=None):
        """Instantiates a Link object

        Args:
            url (str): The URL string either relative or absolute
            parent (Link, optional): If this is None, then the current Link
                will serve as the root, else a parent will be assigned
                to the current Link instance

        Raises:
            ArgumentError: If the arguments are faulty
        """
        # validate args
        if parent:
            if not isinstance(parent, Link):
                raise ArgumentError('Link class should be instantiated with ' \
                    'a valid parent Link object. Got this: %s' %parent)
            url = URLUtils.absolute(parent.url, url)

        # link info
        self.parent = parent
        self.url = URLUtils.normalize(url)
        self.domain = URLUtils.get_domain(url)
        self.is_valid = URLUtils.is_valid(self.url)
        self.id = URLUtils.hash(self.url)
        self.level = 0 if parent is None else parent.level+1

    def __eq__(self, link):
        if isinstance(link, Link):
            return link.url == self.url
        return False

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return '[LINK] URL:%s ; DOMAIN:%s ; IS_VALID:%s ; ID:%s ; LEVEL:%s' \
            %(self.url, self.domain, self.is_valid, self.id, self.level)
