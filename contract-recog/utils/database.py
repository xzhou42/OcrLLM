import traceback
import pymysql
from pymysql.err import IntegrityError
from utils.Log import Log
from datetime import datetime
from utils.get_config_for_env import EnvConfig

env_config = EnvConfig()


class MySqlClient():
    def __init__(self):
        self.host = env_config.mysql_host
        self.user = env_config.mysql_user
        self.password = env_config.mysql_password
        self.database = env_config.mysql_database
        self.create_connection()

    def create_connection(self):
        """ 创建数据库连接 """
        try:  # todo:核对生产的MySQL也是3306吗
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            Log.info("Connection to MySQL DB successful at {}".format(datetime.now()))
        except Exception as e:
            Log.error(f"The error '{e}' occurred")

    def connection_isopen(self):
        """ 判断数据库连接是否存活 """
        return self.connection.open

    def execute_query(self, query, data=None):
        """ 执行SQL查询 """
        # print("connection:",self.connection)
        if self.connection_isopen()==False or not self.connection:
            # print("connection_isopen is open:",mysql_client.connection_isopen())
            self.create_connection()
        else:
            cursor = self.connection.cursor()
            try:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                self.connection.commit()
                Log.info("analysis process insert into database success.")
            except IntegrityError as e:
                Log.error(f"Integrity error: {e}")
            except Exception as e:
                Log.error(traceback.format_exc())
                Log.error(f"The error '{e}' occurred")

    def fetch_data(self, query):
        """ 查询数据并打印结果 """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            # for row in result:
            #     print(row)
            return result
        except Exception as e:
            Log.error(f"The error '{e}' occurred")

# 创建连接
# connection = create_connection()
# print(connection.open)


# 插入数据
# insert_user = "INSERT INTO ocr_llm_anaylysis_result (serial_no,ocr_result,llm_result,json_result) VALUES (%s,%s,%s,%s)"
# user = ("testing_serial","this is ocr_result","this is llm_result","this is json_result")
# execute_query(connection, insert_user, user)

# 查询数据
# select_users = "SELECT * FROM ocr_llm_anaylysis_result"
# fetch_data(connection, select_users)
# #
# # 更新数据
# update_user = "UPDATE users SET name=%s WHERE id=%s"
# new_name = ("Jane Doe", 1)
# execute_query(connection, update_user, new_name)
#
# # 再次查询数据
# fetch_data(connection, select_users)
#
# # 删除数据
# delete_user = "DELETE FROM users WHERE id=%s"
# user_id = (1,)
# execute_query(connection, delete_user, user_id)
#
# # 最后查询数据
# fetch_data(connection, select_users)

# 关闭连接
# connection.close()
