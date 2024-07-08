import pymongo
import requests

JSON_PLACEHOLDER_BASE_URL = 'https://jsonplaceholder.typicode.com/'

# TODO store connection data in environment variables
client = pymongo.MongoClient("mongodb://root:password@localhost:27017/farm?authSource=admin")
db = client["farm"]
posts_collection = db["posts"]
comments_collection = db["comments"]
users_collection = db["users"]

def download_and_save_data(url, collection):
    response = requests.get(url)
    if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
        json_response = response.json()
        collection.insert_many(json_response)
    else: 
        print('error:', response.status_code)

# download posts
download_and_save_data(JSON_PLACEHOLDER_BASE_URL + 'posts', posts_collection)
posts = list(posts_collection.find({}))
print('inserted posts:', len(posts))

# download users
download_and_save_data(JSON_PLACEHOLDER_BASE_URL + 'users', users_collection)
users = list(users_collection.find({}))
print('inserted users:', len(users))

#download comments
for p in posts:    
    download_and_save_data(JSON_PLACEHOLDER_BASE_URL + 'posts/'+ str(p['id']) + '/comments', comments_collection)
comments = list(comments_collection.find({}))
print('inserted comments:',len(comments))