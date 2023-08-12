import os
import logging
import hashlib,json
import time,uuid


class HelperUtils:

    @staticmethod
    def generate_hash(obj: str):
        """
        :param obj:
        :return:
        """
        if obj:
            return hashlib.sha1(obj.encode()).hexdigest()

    @staticmethod
    def get_timestamp():
        time_stamp = int(time.time_ns())
        return time_stamp

    @staticmethod
    def tupple_to_dict(sql_response_list: list, keys: list):
        # keys = ["session_id","cart_id", "item_id", "count","is_active"]
        json_list = []
        print(sql_response_list)
        for tpl in sql_response_list:
            json_dict = {}
            for i in range(len(tpl)):
                json_dict[keys[i]] = tpl[i]
            json_list.append(json_dict)
        return json_list

    @staticmethod
    def create_order_dict(sql_response_list: list):
        order_dict={}
        order_dict["uid"] = sql_response_list[0]["uid"]
        order_dict["session_id"] = sql_response_list[0]["session_id"]
        order_dict["order_id"] = json.loads(sql_response_list[0]["checkout_details"])["order_id"]
        order_dict["checkout_ldts"] = sql_response_list[0]["ldts"]
        order_dict["payment_status"]=0
        order_dict["net_total"] = json.loads(sql_response_list[0]["checkout_details"])["net_total"]
        order_dict["currency"] = "INR"
        order_dict["ldts"] = HelperUtils.get_timestamp()
        return order_dict

#a=[{'uid': 'c88b46f5be0eee347e50a72b0daa371b4cc8a857', 'session_id': 'debtes899997jkjghg-jhhjghvbv86', 'checkout_details': '{"order_id": "00000000-0000-0000-2eec-c24fd7d42425", "available": [{"cost": 595, "count": 5, "item_id": "201816_03_01", "net_cost": 2975}, {"cost": "595", "count": 2, "item_id": "201816_03_02", "net_cost": 1190}], "net_total": 11305, "session_id": "debtes899997jkjghg-jhhjghvbv86", "unavailable": [{"cost": 595, "count": 12, "item_id": "201816_03_01", "net_cost": 7140}], "available_order_no": "00000000-0000-0000-2eec-c24fd7d42425-00", "non_available_order_no": "00000000-0000-0000-2eec-c24fd7d42425-01"}', 'full_order': '[{"cost": 595, "count": 12, "item_id": "201816_03_01", "net_cost": 7140}, {"cost": "595", "count": 2, "item_id": "201816_03_02", "net_cost": 1190}]', 'ldts': 1690645534242521000}]
#print(HelperUtils.create_order_tupple(a))


