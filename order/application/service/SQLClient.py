import os
import logging
import time

from order.utils.SQLUtils import SQLUtils
from order.utils.HelperUtils import HelperUtils
from sqlalchemy.sql import text
from sqlalchemy.exc import *
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer,Table,String,MetaData

logging.getLogger().setLevel(logging.INFO)

class SQLClient:

    def __init__(self) ->None:
        self.sql_conn = "mysql+pymysql://WTrw:WoofandTrill%4012@localhost:3306/external"
        self.engine = create_engine(self.sql_conn)
        self.__table_name="tbl_checkout"

        pass

    def show_checkout(self,table_name,order_model: dict):
        """

        :param table_name:
        :param order_model:
        :return:
        """
        __min_available = 1
        max_retries = 3
        retries = 0
        logging.info("checking if table exist!!...")
        while retries < max_retries:
            try:
                inspect_db = sa.inspect(self.engine)
                is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
                if not is_exist:
                    raise NoSuchTableError
                else:
                    curr_session = sessionmaker(bind=self.engine)
                    session = curr_session()
                    uid = HelperUtils.generate_hash(order_model["uid"])
                    query = SQLUtils.fetch_record(table_name, order_model["session_id"], uid)
                    print(query)
                    cart_list = []
                    response = session.execute(text(query))
                    session.close()
                    logging.info("session closed")
                    for res in response:
                        cart_list.append(res)
                    print(cart_list)
                    return HelperUtils.tupple_to_dict(cart_list, ["uid", "session_id", "checkout_details", "full_order", "ldts", "status"])
            except OperationalError as e:
                logging.error("Error: connection issue {}".format(e))
                retries += 1
                print("in loop")
                time.sleep(1)
            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex
        raise Exception("Could not perform database eration after {} retries".format(max_retries))

    def insert(self, table_name: str, sql_model):
        """

        :param table_name:
        :param sql_model:
        :return:
        """
        try:
            logging.info("checking if table exist!!...")
            inspect_db = sa.inspect(self.engine)
            is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
            if not is_exist:
                raise NoSuchTableError
            else:
                curr_session = sessionmaker(bind=self.engine)
                session = curr_session()
                values = tuple(sql_model.values())
                print(values)
                query = SQLUtils.insert(table_name, values)
                response = session.execute(text(query))
                if response.__dict__['rowcount'] > 0:
                    logging.info("row inserted!..")
                    return True
                raise SQLAlchemyError("Error!...no row affected")
        except DataError as e:
            session.rollback()
            logging.error(f"Insert failed: {e}")
        except Exception as ex:
            session.rollback()
            logging.error(f"issue with query:{ex}")
        finally:
            session.commit()
            session.close()
            logging.info("session closed")

    def update(self, table_name, sql_model):
        """

        :param table_name:
        :param sql_model:
        :return:
        :purpose: updating from cart section
        """
        try:
            logging.info("checking if table exist!!...")
            inspect_db = sa.inspect(self.engine)
            is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
            if not is_exist:
                raise NoSuchTableError
            else:
                curr_session = sessionmaker(bind=self.engine)
                session = curr_session()
                query = SQLUtils.update(table_name, uid=sql_model["uid"], order_id=sql_model["order_id"],
                                        checkout_ldts=sql_model["checkout_ldts"], session_id=sql_model["session_id"],
                                        grand_total=sql_model["grand_total"] ,ldts=sql_model["ldts"])
                print(query)
                response = session.execute(text(query))
                if response.__dict__['rowcount'] > 0:
                    logging.info("row inserted!..")
                    return True
                raise SQLAlchemyError("Error!...no row affected")

        except OperationalError as e:
            logging.error("Error: connection issue {}".format(e))

        except DataError as e:
            session.rollback()
            logging.error(f"Insert failed: {e}")
        except Exception as ex:
            session.rollback()
            logging.error(f"issue with query:{ex}")
        finally:
            session.commit()
            session.close()
            logging.info("session closed")

    def count(self, table_name: str, sql_model: dict):
        """

        :param table_name:
        :param sql_model:
        :return:
        """
        __min_available = 1
        max_retries = 3
        retries = 0
        logging.info("checking if table exist!!...")
        while retries < max_retries:
            try:
                inspect_db = sa.inspect(self.engine)
                is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
                if not is_exist:
                    raise NoSuchTableError
                else:
                    curr_session = sessionmaker(bind=self.engine)
                    session = curr_session()
                    uid = HelperUtils.generate_hash(sql_model["uid"])
                    query = SQLUtils.count(table_name, uid, sql_model["session_id"])
                    logging.info(query)
                    count_list = []
                    response = session.execute(text(query))
                    session.close()
                    logging.info("session closed")
                    for res in response:
                        count_list.append(res[0])
                    print(count_list)
                    return count_list[0]

            except OperationalError as e:
                logging.error("Error: connection issue {}".format(e))
                retries += 1
                print("in loop")
                time.sleep(1)
            except IntegrityError as ix:
                logging.error("key error {}".format(ix))
                raise ix
            except IndexError as ix:
                logging.error("key error {}".format(ix))
                raise Exception(f"Key Error: {ix}")

            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex

        raise Exception("Network error :Could not perform database eration after {} retries".format(max_retries))




#ycmdefme9qg8BSRMSPqV1pKZfH93

#print((SQLClient().show_checkout(order_model)))