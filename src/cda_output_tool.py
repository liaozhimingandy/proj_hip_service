# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2021 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   @Author      : zhiming
#   @Project     : Demo
#   @File Name   : cda_output_tool.py
#   @Created Date: 2021-06-02 17:45
#      @Software : PyCharm
#         @e-Mail: liaozhimingandy@qq.com
#   @Description :
#
# ======================================================================
import pymssql
import sys
import os
import time, datetime
from loguru import logger
from pymssql import _mssql
import uuid
import pandas as pd
from pymssql._pymssql import OperationalError

LIMIT_DATETIME = datetime.datetime(2025, 12, 30)


cda_map = {
    'C0001': '病历概要',
    'C0002': '门（急）诊病历',
    'C0003': '急诊留观病历',
    'C0004': '西药处方',
    'C0005': '中药处方',
    'C0006': '检查报告',
    'C0007': '检验报告',
    'C0008': '治疗记录',
    'C0009': '一般手术记录',
    'C0010': '麻醉术前访视记录',
    'C0011': '麻醉记录',
    'C0012': '麻醉术后访视记录',
    'C0013': '输血记录',
    'C0014': '待产记录',
    'C0015': '阴道分娩记录',
    'C0016': '剖宫产记录',
    'C0017': '一般护理记录',
    'C0018': '病重（病危）护理记录',
    'C0019': '手术护理记录',
    'C0020': '生命体征测量记录',
    'C0021': '出入量记录',
    'C0022': '高值耗材使用记录',
    'C0023': '入院评估',
    'C0024': '护理计划',
    'C0025': '出院评估与指导',
    'C0026': '手术知情同意书',
    'C0027': '麻醉知情同意书',
    'C0028': '输血治疗同意书',
    'C0029': '特殊检查及特殊治疗同意书',
    'C0030': '病危（重）通知书',
    'C0031': '其他知情告知同意书',
    'C0032': '住院病案首页',
    'C0033': '中医住院病案首页',
    'C0034': '入院记录',
    'C0035': '24小时内入出院记录',
    'C0036': '24小时内入院死亡记录',
    'C0037': '首次病程记录',
    'C0038': '日常病程记录',
    'C0039': '上级医师查房记录',
    'C0040': '疑难病例讨论记录',
    'C0041': '交接班记录',
    'C0042': '转科记录',
    'C0043': '阶段小结',
    'C0044': '抢救记录',
    'C0045': '会诊记录',
    'C0046': '术前小结',
    'C0047': '术前讨论',
    'C0048': '术后首次病程记录',
    'C0049': '出院记录',
    'C0050': '死亡记录',
    'C0051': '死亡病例讨论记录',
    'C0052': '住院医嘱',
    'C0053': '出院小结'
}


class CDATool(object):

    def __init__(self, ip='localhost', dbname='CDADB', user='caradigm', pwd='Knt2020@lh', port=1433):
        self.ip = ip
        self.port = port
        self.dbname = dbname
        self.user = user
        self.pwd = pwd
        self.conn = None

    def get_cursor(self):
        try:
            self.conn = pymssql.connect(host=self.ip, port=self.port, user=self.user, password=self.pwd,
                                        database=self.dbname)  # 获取连接
        except(OperationalError,) as e:
            return None
        else:
            return self.conn.cursor()

    def __del__(self):
        # print('连接关闭')
        if self.conn:
            self.conn.close()

    @classmethod
    def collect_data_to_csv(cls, data: dict, file_name='') -> None:
        list_cda_collect_data = []
        for item in cda_map.items():
           list_cda_collect_data.append((item[0], item[1], data.get(item[0], 0)))

        name = ['文档类型代码', '文档类型名称', '文档数量']
        df = pd.DataFrame(columns=name, data=list_cda_collect_data)

        df.to_excel(f'统计数据-{file_name}.xlsx')


def main():
    print(f'{"*" * 10}欢迎使用CDA文档导出工具(version:23.8.2-测试版){"*" * 10}')
    print(f'工具启动时间:{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
    if (LIMIT_DATETIME.timestamp() - datetime.datetime.now().timestamp()) < 0:
        logger.warning('程序已过时,请联系作者进行重新编译!联系邮箱:liaozhimingandy@qq.com')
        # time.sleep(0.1);控制台错位,实际使用不会
        input("按任意键退出...")
        exit(1)
    # cda = CDATool(ip='172.16.33.179', user='caradigm', pwd='Knt2020@lh', dbname='CDADB')

    cursor = None
    cda = None
    width_str = 10
    # 连接数据库
    while not cursor:
        ip = input(f"{'请输入数据库ip地址:'.rjust(width_str, ' ')}")
        # port = input('请输入数据库port(默认为1433):')
        port = 1433
        print(f'{"数据库端口:".rjust(width_str, " ")}1433 (默认为1433)')
        # port处理
        # port = int(port) if port and port.isnumeric() else 1433
        user = input(f"{'请输入数据库用户名:'.rjust(width_str, ' ')}")
        pwd = input(f"{'请输入数据库密码:'.rjust(width_str, ' ')}")
        dbname = input(f"{'请输入数据库名称:'.rjust(width_str, ' ')}")
        logger.info('正在连接数据库...')
        cda = CDATool(ip=ip, port=port, user=user, pwd=pwd, dbname=dbname)
        cursor = cda.get_cursor()
        if not cursor:
            logger.error("数据库连接失败....")
            logger.error("请重新操作....")
    logger.info('连接数据库成功...')
    # 查询条件
    # pid = '00442698'
    # start_datetime = '1889-01-03'
    # end_datetime = '2021-02-03'

    flag = True
    while flag:
        # 参数
        pid = input('请输入患者就诊流水号(VisitNo):')
        AdmissionType = input('请输入患者就诊类型(AdmissionType):')
        # 罗湖区人民医院使用
        # pid = input(f'请输入患者就诊流水号(visit_id):')
        # 删除时间
        # start_datetime = input(f'请输入lastupdate开始日期时间(格式为:2021-01-03):')
        # end_datetime = input(f'请输入lastupdate结束日期时间(格式为:2021-02-03):')
        # admission_type = str(input('请输入AdmissionType:')).strip()

        # sql = f"select [no], PatientName, DocTypeCode, DocContent from(SELECT row_number() over(partition by DocTypeCode order by CreateTime asc) no, [PatientName], DocTypeCode, [DocContent] FROM [CDADocument] where PatientName='{pid}' " \
        #       f"and lastupdate between '{start_datetime}' and '{end_datetime}') as T where T.[no] < 21 "

        # 罗湖区人民医院使用
        # sql = f"""select[no], patient_name, doc_type, content from (SELECT row_number() over(partition by DOCUMENT_TYPE_CODE order by gmt_created asc) no, PATIENT_NAME patient_name, DOCUMENT_TYPE_CODE doc_type, DOCUMENT_CONTENT_CDA content FROM CDA_DOCUMENT where VISIT_id = '{pid}') as T where T.[no] < 10000"""
        # sql = f"""select[no], patient_name, doc_type, content from (SELECT row_number() over(partition by DOCUMENT_TYPE_CODE order by gmt_created asc) no, PATIENT_NAME patient_name, DOCUMENT_TYPE_CODE doc_type, DOCUMENT_CONTENT_CDA content FROM CDA_DOCUMENT where VISIT_id = '{pid}' and CDA_DOCUMENT_TYPE_CODE in('C0006', 'C0007', 'C0013', 'C0022')) as T where T.[no] < 10000"""

        # 中山七院专用
        sql = f"SELECT row_number() over(partition by DocTypeCode order by CreateTime asc) no, [PatientName], DocTypeCode, [DocContent] " \
              f"FROM [CDADocument]" \
              f"where VisitNo='{pid}' and AdmissionType = '{AdmissionType}' and DocTypeCode <> 'C0006'"
        # print(f'执行的sql语句为:\n{sql}')
        cursor.execute(sql)

        # if not os.path.exists('cda'):
        #     os.makedirs('cda')
        logger.info(f"您的查询语句为:\n{sql.replace('//n', '')}")
        logger.info(f'{"*" * 5}正在生成中,请稍等{"*" * 5}')
        for row in cursor:
            # file_dir = f'cda\{row[1]}\EMR-SD-{row[2][-2:]}-{cda_map.get(row[2], "未知")}'
            file_dir = f'cda/{row[1]}'
            # if not os.path.exists(f'cda\{row[1]}'):
            #     os.makedirs(f'cda\{row[1]}')
            # if not os.path.exists(f'cda\{row[1]}\EMR-SD-{row[2][-2:]}-{cda_map.get(row[2])}'):
            #     os.makedirs(f'cda\{row[1]}\EMR-SD-{row[2][-2:]}-{cda_map.get(row[2])}')
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            # 人民
            # tmp_file_name =  f'EMR-SD-{row[2][-2:]}-{cda_map.get(row[2], "未知")}-{row[1]}-T01-{str(row[0]).rjust(3, "0")}.xml'
            # tmp_file_name = f'EMR-SD-{row[2][-2:]}-{cda_map.get(row[2], "未知")}-T01-{str(row[0]).rjust(3, "0")}.xml'
            # 中山七院
            tmp_file_name = f'EMR-SD-{row[2][-2:]}-{cda_map.get(row[2], "未知")}-{row[1]}-T01-{str(row[0]).rjust(3, "0")}.xml'
            # print(tmp_file_name)
            with open(file=f'{file_dir}/{tmp_file_name}', encoding='utf-8', mode='w', newline='') as f:
                f.writelines(row[3])
            logger.info(f'完成:{tmp_file_name}')


        ######################################汇总数据#####################################################
        # print(f'######################################执行第二步,统计数据######################################')
        # sql_summary = f"select CDA_DOCUMENT_TYPE_CODE, CDA_DOCUMENT_TYPE_NAME, count(1) [count] from [dbo].[CDA_DOCUMENT](nolock) where VISIT_id = '{pid}' group by  CDA_DOCUMENT_TYPE_CODE, CDA_DOCUMENT_TYPE_NAME"
        # cursor.execute(sql_summary)
        # dict_tmp = {}
        # for row in cursor:
        #     dict_tmp[row[0]] = row[2]
        # logger.info(f"您的统计语句为:\n{sql_summary.replace('//n', '')}")
        # CDATool.collect_data_to_csv(data=dict_tmp, file_name=pid)
        print(f'######################################统计完毕######################################')
        ###############################################################################################
        yes = input('是否继续?(否请填N,继续任意键):')
        if yes.lower() == 'n':
            flag = False

        # 检查过时
        if (LIMIT_DATETIME.timestamp() - datetime.datetime.now().timestamp()) < 0:
            logger.warning('程序已过时,请联系作者进行重新编译!联系邮箱:liaozhimingandy@qq.com')
            flag = False

    input("按任意键退出...")


if __name__ == "__main__":
    if hasattr(sys, 'frozen'):
        os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    main()
    # CDATool.collect_data_to_csv(data={'C0001': 0})