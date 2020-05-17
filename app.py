from time import sleep
from modules.twitter_client.twitter_client import TwitterClient
from modules.db.mongodb import MongoDB
from modules.grpc.client import GrpcClient
from dotenv import load_dotenv
from os import getenv


def run():
    load_dotenv()

    REFRESH_INTERVAL = int(getenv('REFRESH_INTERVAL')) if getenv('REFRESH_INTERVAL') != None else 60

    DB_NAME = getenv('DB_NAME')
    DB_CONNECTION_STRING = getenv('DB_CONNECTION_STRING')

    db = MongoDB(DB_CONNECTION_STRING)
    db.connect_db(DB_NAME)

    grpc = GrpcClient(getenv('SERVICE_GRPC_STORM_URL'))

    consumer_key = getenv("TW_CONSUMER_KEY")
    consumer_secret = getenv("TW_CONSUMER_SECRET")
    access_token = getenv("TW_ACCESS_TOKEN")
    access_secret = getenv("TW_ACCESS_SECRET")

    tw = TwitterClient(
        consumer_key,
        consumer_secret,
        access_token,
        access_secret,
        db,
        grpc
    )

    db.select_col('mentions')

    while True:
        last_mention = db.find_last_object()
        last_mention_id = last_mention['latest_mention_id'] if last_mention != None else 0
        tw.get_mention(last_mention_id)
        sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    run()
