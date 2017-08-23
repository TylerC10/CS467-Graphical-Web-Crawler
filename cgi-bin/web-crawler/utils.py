import re
import hashlib
import urlparse

from lxml import html
from lxml.html.clean import Cleaner


class HTMLUtils(object):
    #Utility class for HTML manipulations. All methods in this class are static methods. No need to instantiate.
    HTML_CLEANER = Cleaner(**{
        'scripts': True,
        'javascript': True,
        'comments': True,
        'style': True,
        'inline_style': True,
        'meta': True,
        'embedded': True,
        'remove_unknown_tags': True
    })

    @staticmethod
    def html_to_text(html_content):
        """Retrieves text content from a given HTML string

        In the process of extracting the text content from the given HTML
        string, all javascript content, style content, comments,
        embedded objects, tags, etc. are removed

        Args:
            html_content (str): The input HTML string

        Returns:
            unicode: The clean text output, extracted from the given HTML string
        """
        cleaned_html_content = HTMLUtils.HTML_CLEANER.clean_html(html_content)
        text = html.fromstring(cleaned_html_content).text_content()
        text = re.sub(r'/\s+/g', ' ', text).strip()
        return text


class URLUtils(object):
    #Utility class for HTML manipulations. All methods in this class are static methods. No need to instantiate.

    @staticmethod
    def absolute(base_url, url):
        """Makes a relative URL into an absolute URL

        Args:
            base_url (str): The full/absolute URL, for reference
            url (str): The target URL which is to be made an absolute URL

        Returns:
            str: An absolute URL
        """
        return urlparse.urljoin(base_url, url)

    @staticmethod
    def hash(url):
        """Makes a hash (32-character string) of the given URL
        with the MD5 algorithm

        Args:
            url (str): The target URL which is to be hashed

        Returns:
            str: A 32-character string
        """
        return hashlib.md5(url).hexdigest()

    @staticmethod
    def get_domain(url):
        """Returns the domain of the given URL

        Args:
            url (str): The target URL whose domain is required

        Returns:
            str: The domain of the given URL
        """
        return urlparse.urlparse(url).netloc

    @staticmethod
    def normalize(url):
        """Normalizes a given URL, removing unwanted parts like fragments

        Args:
            url (str): The target URL which is to be normalied

        Returns:
            str: A normalized URL
        """
        return urlparse.urldefrag(url)[0]

    @staticmethod
    def is_valid(url):
        """Validates if a given URL is valid or not

        Args:
            url (str): The target URL which is to be validated

        Returns:
            bool: True, if the URL is valid; else False
        """
        try:
            result = urlparse.urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
