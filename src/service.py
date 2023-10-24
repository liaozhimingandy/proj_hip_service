import json
import os.path
import time
from xml.etree import ElementTree as et

# 定义XML命名空间
namespace = {'xmlns': 'urn:hl7-org:v3'}


def update_demo_base_info(desc_dir_path: str):
    # 统一请求ID
    import uuid
    id_msg = str(uuid.uuid4()).replace('-', '')
    import os
    gmt_created = time.strftime('%Y%m%d%H%M%S')

    id_sender, id_receiver = '12361', '107'

    import glob
    for file_name in glob.glob(desc_dir_path):
        doc = et.parse(file_name)
        root = doc.getroot()
        root.find('xmlns:id', namespace).set('extension', id_msg)
        root.find('xmlns:creationTime', namespace).set('value', gmt_created)
        root.find('xmlns:sender/xmlns:device/xmlns:id/xmlns:item', namespace).set('extension', id_sender)
        root.find('xmlns:receiver/xmlns:device/xmlns:id/xmlns:item', namespace).set('extension', id_receiver)

        # 创建文件夹
        base_file_name = os.path.basename(file_name)
        result_file = f"result-{gmt_created[:8]}/{base_file_name[:-6].replace('-F', 'F') if ('F' in base_file_name[:-6]) else base_file_name[:-6]}"
        if not os.path.exists(result_file):
            os.makedirs(result_file)

        # 保存到文件
        et.register_namespace('', 'urn:hl7-org:v3')
        doc.write(f"{result_file}/{base_file_name}", encoding="utf-8", short_empty_elements=True)

        print(f"已处理:{file_name}")

    print(f"共处理{len(glob.glob(dir_path))}条数据")


def update_demo_parm():
    list_file_path = ["EMR-PL-04-个人信息查询服务-T", "EMR-PL-07-医疗卫生机构（科室）信息查询服务-T",
                      "EMR-PL-10-医疗卫生人员信息查询服务-T", "EMR-PL-13-术语查询服务-T",
                      "EMR-PL-15-电子病历文档检索服务-T",
                      "EMR-PL-16-电子病历文档调阅服务-T", "EMR-PL-19-就诊卡信息查询服务-T",
                      "EMR-PL-22-门诊挂号信息查询服务-T", "EMR-PL-25-住院就诊信息查询服务-T",
                      "EMR-PL-28-住院转科信息查询服务-T", "EMR-PL-31-出院登记信息查询服务-T",
                      "EMR-PL-34-医嘱信息查询服务-T", "EMR-PL-37-检验申请信息查询服务-T",
                      "EMR-PL-40-检查申请信息查询服务-T", "EMR-PL-43-病理申请信息查询服务-T",
                      "EMR-PL-46-输血申请信息查询服务-T", "EMR-PL-49-手术申请信息查询服务-T",
                      "EMR-PL-52-号源排班信息查询服务-T", "EMR-PL-55-门诊预约状态信息查询服务-T",
                      "EMR-PL-58-检查预约状态信息查询服务-T", "EMR-PL-60-医嘱执行状态信息查询服务-T",
                      "EMR-PL-62-检查状态信息查询服务-T", "EMR-PL-64-检验状态信息查询服务-T",
                      "EMR-PL-79-手术排班信息查询服务-T", "EMR-PL-81-手术状态信息查询服务-T"]

    with open('template-service-params.json', 'r', encoding="UTF-8") as fp:
        dict_parm = json.load(fp)

    for e in list_file_path:
        path_file = f'result-{time.strftime("%Y%m%d")}\\{e}\\{e}01.xml'
        tree = et.parse(path_file, et.XMLParser())
        root = tree.getroot()

        dict_key = e[:9]
        value = dict_parm.get(dict_key)
        # print(root.find('xmlns:controlActProcess/xmlns:queryByParameter/xmlns:parameterList/xmlns:id', namespaces=namespace)

        if dict_key in ("EMR-PL-52", ):
            root.find(value.get('path').strip(), namespaces=namespace).set(value.get("node"), value.get("value"))
            root.find(value.get('path2').strip(), namespaces=namespace).set(value.get("node2"),  value.get("value2"))
        else:
            root.find(value.get('path').strip(), namespaces=namespace).set(value.get("node"),  value.get("value"))

        # 保存到文件
        et.register_namespace('', 'urn:hl7-org:v3')
        tree.write(path_file, encoding="utf-8", short_empty_elements=True)
        print(f"已处理完成:{path_file}")

    print(f'处理完毕,共计{len(list_file_path)}个文件!')


if __name__ == "__main__":
    # 读取参数
    from test_deal_file import test3, test1
    test3()

    dir_path = r'D:\BaiduNetdiskWorkspace\项目资料\深圳市中山大学附属第七医院\互联互通五乙-交互服务-demo\*.xml'
    update_demo_base_info(dir_path)
    update_demo_parm()

    #生成参数说明
    test1()