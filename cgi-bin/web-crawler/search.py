from datetime import datetime

from web import HTMLPage, Link
from persist import Postgres

from errors import ArgumentError
from errors import PersistenceExecuteError
import logging

class WebCrawler(object):
    #A Crawler instance that is attached to a User (by his/her UserID) With this instance, BFS/DFS can be performed from any given URL and the results can be retrieved or optionally persisted on a database (with the UserID being a part of the primary key of most tables)
    def __init__(self, db_config, user_id):
        #Associates the WebCrawler instance to a User - Args: user_id (str): A string that represents a UserID. Raises: PersistenceConnectionError: For DB Connection issues
        self.db = Postgres(**db_config)
        self.user_id = user_id

    def search(self, search_code, search_type, start_url, max_level,
    stop_words=[], allowed_domains=[], persist=True):
        """Starts from the given URL, performs a Breadth First Search (BFS)
        or a Depth First Search (DFS) and continues indefinitely until
        a maximum level is reached or until one of the given stop words are
        encountered

        Args:
            search_code (str): A unique sting identifying the
                current search request
            search_type (str): Allowed values are "BFS" or "DFS"
            start_url (str): Search starting point
            max_level (int): The maximum level until which the search should
                be performed
            stop_words (list(str), optional): The list of words which is to be
                checked for to halt the current search
            allowed_domains (list(str), optional): The list of domains to
                restrict the URLs to, while performing the search
            persist (bool, optional): If True, the search results will be
                persisted in the database

        Returns:
            set(str): A list of unique Link objects encountered while performing
                the breadth first search

        Raises:
            ArgumentError: If arguments are faulty
            PersistenceExecuteError: For DB Query Execution issues
            PersistenceError: For any other DB related issue
        """
        # validate args
        if not isinstance(search_type, str) or \
        search_type.upper() not in ['BFS', 'DFS']:
            raise ArgumentError('Param "search_type" must be either of ' \
                '"bfs" or "dfs". Got: %s' %search_type)
        if not isinstance(start_url, str):
            raise ArgumentError('Param "start_url" must be a string. ' \
                'Got: %s' %start_link.url)
        start_link = Link(start_url)
        if not start_link.is_valid:
            raise ArgumentError('Param "start_url" must be a valid URL. ' \
                'Got: %s' %start_link.url)
        if not isinstance(max_level, int):
            raise ArgumentError('Param "max_level" must be an integer. ' \
                'Got: %s' %max_level)

        # add the current domain to the list of allowed domains
        if not start_link.domain in allowed_domains:
            allowed_domains.append(start_link.domain)

        if persist:
            search_info = {
                'search_code': search_code,
                'search_type': search_type,
                'start_url': start_url,
                'max_level': max_level,
                'crawled_date_time': datetime.today()
            }

            # save job details to DB
            try:
                self.db.insert('CRAWL.INFO', search_info)
                self.db.commit()
            except PersistenceExecuteError as err:
                self.db.rollback()
                logging.error('Insertion to CRAWL.INFO table failed for user: %s' \
                    %self.user_id)
                raise err

        # initiate the data structures
        visited = set()
        queue = [ start_link ]
        stop_word_hit = False

        # perform search
        while queue and not stop_word_hit:
            # depending on whether the search type is BFS/DFS
            # retrieve from top or bottom of the queue
            link = queue.pop(0) if search_type == 'BFS' else queue.pop()

            if link.is_valid and link not in visited:
                # visit the current link
                visited.add(link)

                if persist:
                    # save the link to DB
                    try:
                        link_data = {
                            'search_code': search_code,
                            'id': link.id,
                            'url': link.url,
                            'level': link.level,
                            'parent_id': link.parent and link.parent.id
                        }
                        self.db.insert('CRAWL.DATA', link_data)
                    except PersistenceExecuteError as err:
                        logging.error('Insertion to CRAWL.DATA table failed for user: %s' \
                            %self.user_id)
                        raise err

                # parse current page and get all child links
                page = HTMLPage(link)
                if page.status_code == 200 and link.level < max_level:
                    queue.extend(page.get_links(allowed_domains))
                logging.info(page)

                # check if the current page has one of the given stop words
                for word in stop_words:
                    stop_word_hit = stop_word_hit or page.has_word(word)

        self.db.commit()
        return visited
