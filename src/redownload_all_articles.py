import db_layer
import utils

if __name__ == '__main__':
    db_layer.redownload_all_articles(utils.PATH_TO_SHARE_DB) 
    
