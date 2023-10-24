import json
import pymssql


def main():
    with open('cda.txt', encoding='utf-8', mode='r') as fp:
        data = json.load(fp)
        print(data)


def test():
    # 连接参数
    server = '10.1.8.12'
    database = 'HIPMonitor'
    username = 'sa'
    password = 'p@ssw0rd'

    # 建立连接
    conn = pymssql.connect(server=server, database=database, user=username, password=password)

    # 创建游标对象
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute("select ApplicationId from Tbl_Application")

    # 获取查询结果
    result = cursor.fetchall()

    list_services = ['8CBE4DDA-3821-4F75-9EBC-28C5D2161110', '9C96A835-B1B1-489E-952B-DD3DB2A59422','57674AE0-A804-4E95-901E-BBF7B7BD750A', 'C89B382E-3532-414B-94AD-2F598EB4198F']
    for item in result:
        for e in list_services:
            sql = f"insert into Tbl_Subscription(applicationid, serviceid) values(%s, %s)"
            try:
                cursor.execute(sql, (item[0], e))
            except(Exception, ):
                pass
            else:
                print(sql)

    conn.commit()


if __name__ == "__main__":
    test()