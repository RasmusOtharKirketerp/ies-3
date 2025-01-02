import db_layer
from utils import EXCLUDE_URLS, PATH_TO_SHARE_DB

def remove_urls():
   db_layer.delete_excluded_urls_from_db(EXCLUDE_URLS, PATH_TO_SHARE_DB)


if __name__ == '__main__':
    remove_urls()