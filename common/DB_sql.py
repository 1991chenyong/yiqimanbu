# -*- coding:UTF-8 -*-
import pymysql


# # 链接数据库
# def connect_mysql(request):
#     # 数据库连接账号密码
#     config = {
#         "host": "192.168.0.202",
#         "user": "ltms_all",
#         "passwd": "%5*D06#E1^",
#         "database": "tms"
#     }
#     # 创建数据库
#     db = pymysql.connect(**config)
#     # 创建游标
#     cursor = db.cursor()
#     # 创建一个空字典接收返回的数据
#     data_dict = {}
#     search_dict = request.param
#     if isinstance(search_dict, dict):
#         for key, value in search_dict.items():
#             print(value)
#             search_num = cursor.execute(value)
#             if search_num:
#                 value = cursor.fetchall()
#                 data_dict[key] = value[0][0]
#             else:
#                 write_error_log("执行sql查询语句没有返回任何结果")
#     print("未进入")
#     yield data_dict
#     print("进入")
#     # 关闭游标和数据库
#     cursor.close()
#     db.close()


class DbConnect(object):

    def __init__(self):
        # 数据库连接账号密码
        config = {
            "host": "192.168.0.202",
            "user": "ltms_all",
            "passwd": "%5*D06#E1^",
            "database": "tms"
        }
        # 创建数据库
        self.connection = pymysql.connect(**config)
        # 创建游标
        self.cursor = self.connection.cursor()

    def update_sql(self, *args):
        try:
            sql = "UPDATE %s SET %s=%s WHERE %s='%s';" % (args)
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print('Error:%s' % e)

    def delete_sql(self, *args):
        try:

            sql = "DELETE FROM %s WHERE %s='%s';" % (args)
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print('Error:%s' % e)

    def select_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            result = self.cursor.fetchall()
            return result[0]
        except Exception as e:
            print('Error:%s' % e)

    def close_conn(self):
        self.connection.close()
        self.cursor.close()


if __name__ == "__main__":
    shipping_no_sql = 'SELECT shipping_no from warehouse_handover where handover_no = "REC202103090006";'
    shipping_no = DbConnect().select_sql(shipping_no_sql)[0]
    print(shipping_no)
    sql = 'SELECT id,send_time from shipping where shipping_no = "%s";' % shipping_no
    data_tuple = DbConnect().select_sql(sql)
    id = data_tuple[0]
    send_time = data_tuple[1]
    print(id, send_time)










