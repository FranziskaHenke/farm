from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import datetime
import json
from bson import json_util


app = FastAPI()

origins = [
    "http://0.0.0.0:3000",
    "http://localhost:3000"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


mongo_client = None
def get_client():
    """
    Setup a mongo client for the site
    :return:
    """
    global mongo_client
    if bool(mongo_client):
        return mongo_client
    mongo_client = MongoClient("mongodb://root:password@mongo:27017/farm?authSource=admin")
    return mongo_client

@app.get('/')
async def home():
    return {'message': 'Hello World'}

@app.get('/user_post_comments_cnt/{userId}')
async def get_user_posts_counts(userId: int): 
    filter = {'userId': userId}
    client = get_client()
    db = client['farm']
    posts = list(db['posts'].find(filter))
    posts_cnt = len(posts)
    post_ids = [p['id'] for p in posts]
    filter = {'postId': {'$in':post_ids}}
    comments_cnt = db['comments'].count_documents(filter)
    return {'posts_cnt': posts_cnt, 'comments_cnt': comments_cnt}


@app.get('/turbine/{turbine_id}')
async def get_turbine_data(
        turbine_id: str, 
        start_date: str = Query(..., description="Timestamp Format DD.MM.YYYY HH24:MI"), 
        end_date: str = Query(..., description="Timestamp Format DD.MM.YYYY HH24:MI")
    ) -> list: 
    print(start_date)
    print(end_date)
    start_date_tst = datetime.datetime.strptime(start_date, '%d.%m.%Y %H:%M')
    end_date_tst = datetime.datetime.strptime(end_date, '%d.%m.%Y %H:%M')
    client = get_client()
    db = client['farm']
    print(start_date_tst)
    filter = {'Turbine': turbine_id, 'Dat/Zeit': {'$gte': start_date_tst}, 'Dat/Zeit': {'$lte': end_date_tst}}
    turbine_data = list(db['turbines'].find(filter))
    return json.loads(json_util.dumps(turbine_data))
