"""Entry point for the application"""
from api import start_api
from database.collections_script import create_collections

WITH_API = False
RUN_CREATE_COLLECTION = True

def main():
    """Entry function for starting all the application"""
    if WITH_API:
        start_api()

    if RUN_CREATE_COLLECTION:
        create_collections()

if __name__ == '__main__':
    main()
