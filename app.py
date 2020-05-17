from time import sleep
from modules.twitter_client.twitter_client import TwitterClient
from modules.db.mongodb import MongoDB
from modules.grpc.client import GrpcClient
from dotenv import load_dotenv
from os import getenv


def run():
    load_dotenv()

    DB_NAME = getenv('DB_NAME')
    db = MongoDB()
    db.connect_db(DB_NAME)
    db.select_col('environment')

    grpc = GrpcClient(getenv('SERVICE_GRPC_STORM_URL'))

    env = db.find_last_object()
    consumer_key = env['consumer_key']
    consumer_secret = env['consumer_secret']
    access_token = env['access_token']
    access_secret = env['access_secret']

    tw = TwitterClient(
        consumer_key,
        consumer_secret,
        access_token,
        access_secret,
        db,
        grpc
    )

    db.select_col('mentions')
    if db.collection.count() == 0:
        data = {'user_id': 0, 'url_links': 'null',
                'command': 'null', 'latest_mention_id': 0}
        db.insert_first_data(data)

    while True:
        last_mention = db.find_last_object()
        last_mention_id = last_mention['latest_mention_id']

        since_id = tw.get_mention(last_mention_id)

        if last_mention_id == since_id:
            print(f"No new mention")

        sleep(30)


if __name__ == "__main__":
    run()
