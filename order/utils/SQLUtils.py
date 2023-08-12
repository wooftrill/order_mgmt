import os
import logging
logging.getLogger().setLevel(logging.INFO)


class SQLUtils:
    def __init__(self):
        pass

    @staticmethod
    def fetch_record(table_name: str , session_id: str, uid: str):
        return f"select * from external.{table_name} where session_id='{session_id}' and uid='{uid}' and status=0 ;"

    @staticmethod
    def insert(table_name : str, args ):
        return f"INSERT INTO {table_name} VALUES {args};"

    @staticmethod
    def update(table_name: str,order_id: str,checkout_ldts,ldts, net_total,uid:str, session_id: str):
        return f"Update external.{table_name} SET order_id='{order_id}', checkout_ldts={checkout_ldts},ldts={ldts}, net_total={net_total} where uid='{uid}'and session_id='{session_id}' and payment_status=0;"

    @staticmethod
    def count(table_name: str, uid: str,session_id: str):
        return f"SELECT COUNT(*) from external.{table_name} WHERE uid='{uid}'and session_id='{session_id}'and payment_status=0;"

