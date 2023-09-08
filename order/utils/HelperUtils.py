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
        order_dict["grand_total"] = json.loads(sql_response_list[0]["checkout_details"])["grand_total"]
        order_dict["currency"] = "INR"
        order_dict["ldts"] = HelperUtils.get_timestamp()
        return order_dict

#a=[{'uid': '36141bb3a7ccccb7c733e7bff6b697abe84da8c6', 'session_id': 'ghsgdhsh7873673hwgikk', 'checkout_details': '{"total": 505.75, "net_cost": 595.0, "order_id": "00000000-0000-0000-2f05-1ee3ab179ca2", "available": [{"cost": "595", "count": 1, "item_id": "201816_03_01", "net_cost": 595}], "net_total": 595, "session_id": "ghsgdhsh7873673hwgikk", "grand_total": 571.42, "unavailable": [], "delvery_cost": 65.67, "wt_discount_id": "DISCOUNT001", "wt_discount_prtn": 15, "delvery_addrss_id": "550e8400-e29b-41d4-a716-446655440000", "available_order_no": "00000000-0000-0000-2f05-1ee3ab179ca2-00"}', 'full_order': '[{"cost": "595", "count": 1, "item_id": "201816_03_01", "net_cost": 595}]', 'ldts': 1694074128971500200, 'status': 0}]
#print(HelperUtils.create_order_dict(a))


