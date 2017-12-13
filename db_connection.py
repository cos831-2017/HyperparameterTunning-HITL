import redis
import pymonetdb
from config import RDB_RESULTS_HOST, RDB_RESULTS_PORT, RDB_RESULTS_NO
from config import MONEDB_USERNAME, MONETDB_PASSWORD, MONETDB_HOST, MONEDB_PROV_DB

def redis_db_connection():
    connection = redis.StrictRedis(
        host = RDB_RESULTS_HOST,
        port = RDB_RESULTS_PORT,
        db = RDB_RESULTS_NO,
        charset = "utf-8",
        decode_responses = True)
    return connection

rdb = redis_db_connection()


def monet_db_connection():
    connection = pymonetdb.connect(
        username = MONEDB_USERNAME,
        password = MONETDB_PASSWORD,
        hostname = MONETDB_HOST,
        database = MONEDB_PROV_DB)
    return connection

