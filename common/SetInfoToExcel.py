#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
@author: tanglei
@contact: tanglei_0315@163.com
@file: SetInfoToExcel.py
@time: 2019/1/14 11:26
'''
#导入第三方模块
from openpyxl import Workbook
import os
import time
import shutil
#导入自定义的模块
from common.GetMeetingInfo import GetMeetingInfo,GetDetailedInformation
from common.GetMeetingInfo import GetMeetingInfoApi,GetInfoApiParams,Headers,LoginApiParams,MeetingLoginApi
from common.GetUserInfo import GetUserAll
from common.logger import logger
#设置当前时间的变量
time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
#设定上一层目录
path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
excel_file = os.path.join(path,"MeetingDaily.xlsx")
excel_backup_file = os.path.join(path,"excel_backup\MeetingDaily_%s.xlsx" %(time))
MeetingApi = GetMeetingInfo(MeetingLoginApi, LoginApiParams, Headers)
MeetingApi.Login()
MeetingApi = GetMeetingInfo(GetMeetingInfoApi, GetInfoApiParams, Headers)
MeetingApi.GetInfo()
MeetingInfo = GetDetailedInformation(MeetingApi.GetInfo())
#会议个数
MeetingLen = MeetingInfo.List_len()

def SetInfoToExcel():
    if os.path.isfile(excel_file):
        shutil.move(excel_file,excel_backup_file)
    Header = {"A1":"序号","B1":"会议号","C1":"会议时间","D1":"持续时间","E1":"端到端总体合格率","F1":"平均合格率","G1":"端到端最高合格率","H1":"端到端最低合格率","I1":"不合格端到端明细数据","J1":"开会方数","K1":"用户列表","L1":"设备类型"}
    wb = Workbook()
    ws = wb.active
    for k,v in Header.items():
        ws[k] = v
        wb.save(excel_file)
    for item in range(MeetingLen):
        Body = {"A%d" % (item + 2): item + 1,
                "B%d" % (item + 2): MeetingInfo.GetMeetingNumber()[item],
                "C%d" % (item + 2): MeetingInfo.GetMeetingTime()[item],
                "D%d" % (item + 2): MeetingInfo.GetMeetingDuration()[item],
                "E%d" % (item + 2): MeetingInfo.GetPtoPTotal()[item],
                "F%d" % (item + 2): "丢包:%s\n空音包:%s" % (
            MeetingInfo.PacketLossAverage()[item], MeetingInfo.SoundPacketLossAverage()[item]),
                "G%d" % (item + 2): "丢包:%s\n空音包:%s" % (
                MeetingInfo.PacketLossMax()[item], MeetingInfo.SoundPacketLossMax()[item]),
                "H%d" % (item + 2): "丢包:%s\n空音包:%s" % (
                MeetingInfo.PacketLossMin()[item], MeetingInfo.SoundPacketLossMin()[item]),
                "I%d" % (item + 2): "\n".join(MeetingInfo.DetailData()[item]),
                "J%d" % (item + 2): MeetingInfo.MeetingPeopleNumber()[item],
                "K%d" % (item + 2): "\n".join(GetUserAll()[0][item]),
                "L%d" % (item + 2): "\n".join(GetUserAll()[1][item])}
        for k,v in Body.items():
            ws[k] = v
            wb.save(excel_file)