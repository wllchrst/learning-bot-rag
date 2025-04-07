from api import start_api
from database import create_collections

WITH_API = False
RUN_CREATE_COLLECTION = True

def main():
    if WITH_API:
        start_api()
    
    if RUN_CREATE_COLLECTION:
        create_collections()        
        
if __name__ == '__main__':
    main()