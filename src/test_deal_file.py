import json
import re

from loguru import logger


def test_insert_db(*args):
    import pymssql

    # 连接参数
    server = '10.1.8.12'
    database = 'HIP_MSG'
    username = 'sa'
    password = 'p@ssw0rd'

    # 建立连接
    conn = pymssql.connect(server=server, database=database, user=username, password=password)

    # 创建游标对象
    cursor = conn.cursor()

    insert_query = "INSERT INTO tmp2 (t1, t2, t3, t4) VALUES (%s, %s, %s, %s)"
    insert_data = (args[0], args[1], args[2], args[3])
    cursor.execute(insert_query, insert_data)

    # 提交事务
    conn.commit()

    # 关闭游标
    cursor.close()


def test():
    file_path = r'D:\data\WeChat\WeChat Files\wxid_oviup54trb2i21\FileStorage\File\2023-10\230920'
    import os
    import datetime
    items = os.listdir(file_path)
    for item in items:
        gmt = datetime.datetime.strptime(f'20{item.split("_")[0]}', '%Y%m%d%H%M%S').strftime("%Y-%m-%d %H:%M:%S")
        event_code = f'E{item.split("_")[2]}'
        logger.debug((gmt, item, event_code))

        with open(os.path.join(file_path, item), 'r') as fp:
            data = fp.read()
            d1 = re.search(r'入参(.|\n)*>', data, re.M|re.I).group().replace(r'入参:', '').strip()
            d2 = re.search(r'出参(.|\n)*access_token', data, re.M | re.I).group().replace(r'出参:', '').replace(r'access_token', '').strip()

            test_insert_db(event_code, d1, d2, gmt)

        # break

# 生成参数说明
def test1():
    with open("template-service-params.json", "r", encoding="UTF-8") as fp:
        data = json.load(fp)

    items = []
    for item in data.items():
        # logger.debug(f"({item[1].get('comment').split('->')[0]}, {item[1].get('value')})")
        if item[0] == "EMR-PL-52":
            items.append((item[1].get('service'), (item[1].get('comment').split('->')[0], item[1].get('comment2').split('->')[0]),
                                                   (item[1].get('value'), item[1].get('value2'))))
            items.append((item[1].get('service'),
                          (item[1].get('comment').split('->')[0], item[1].get('comment2').split('->')[0]),
                          ('0000', '0000')))
        else:
            items.append((item[1].get('service'), item[1].get('comment').split('->')[0], item[1].get('value')))
            items.append((item[1].get('service').replace('T', 'F'), item[1].get('comment').split('->')[0], '0000'))
    import time
    import pandas as pd
    df = pd.DataFrame(data=items, columns=['service', 'comment', "value"])

    file_name = f"入参说明-{time.strftime('%Y%m%d')}.xlsx"
    df.to_excel(file_name, index=False)

    logger.info(file_name)


def test2():
    with open("template-service-params.json", "r", encoding="UTF-8") as fp:
        data = json.load(fp)

    items = []
    for item in data.items():
        items.append((item[1].get('service'), item[1].get('comment'), item[1].get('value')))

    import pandas as pd
    df = pd.DataFrame(data=items, columns=['服务名称', '参数名称', "参数值"])

    df.to_excel("参数模板.xlsx", index=False)


# 从excel文件读取参数更新到参数模板
def test3():
    import pandas as pd
    df = pd.read_excel("参数模板.xlsx")
    list_data= df.values.tolist()

    with open("template-service-params.json", "r", encoding="UTF-8") as fp:
        data = json.load(fp)

    for item in list_data:
        if item[0][:9] == 'EMR-PL-52':
            data.get(f'{item[0][:9]}')['value'] = item[2].split(',')[0].strip()
            data.get(f'{item[0][:9]}')['value2'] = item[2].split(',')[1].strip()
        else:
            data.get(f'{item[0][:9]}')['value'] = item[2]

    with open("template-service-params.json", "w", encoding="UTF-8") as fp:
        fp.write(json.dumps(data))

    logger.info("更新参数模板成功!")


if __name__ == "__main__":
    # test()
    # test1()
    test3()
