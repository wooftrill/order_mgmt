import json
import os
import logging
from order.application.service.SQLClient import SQLClient
from order.utils.HelperUtils import HelperUtils
from dataclasses import asdict
from order.config.config import TABLE


class SQLOrmService(SQLClient):
    def __init__(self):
        super().__init__()
        self.__order_table=TABLE["order"]
        self.__checkout_table=TABLE["checkout"]

    def generate_order(self,checkout_model:dict):
        """

        :param checkout_model:
        :return:
        """
        logging.info("order generation function triggered..")
        try:
            if self.show_checkout(self.__checkout_table,checkout_model):
                logging.info("Checkout Item found....")
                print("jjjj")
                print(self.show_checkout(self.__checkout_table,checkout_model))
                check_out_obj = HelperUtils.create_order_dict(self.show_checkout(self.__checkout_table,checkout_model))
                if check_out_obj:
                    logging.info("Validity test passed !!!")
                    if self.count("tbl_order",checkout_model)> 0:
                        logging.info("updating the table")
                        if self.update(self.__order_table,check_out_obj):
                            return check_out_obj
                    else:
                        logging.info("inserting")
                        if self.insert(self.__order_table,check_out_obj):
                            return check_out_obj
            else:
                return False

        except Exception as e:
            logging.error(e)


sql_orm_service = SQLOrmService()

