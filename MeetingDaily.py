#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
@author: tanglei
@contact: tanglei_0315@163.com
@file: MeetingDaily.py
@time: 2019/1/14 11:24
'''
#导入自定义模块
from common.logger import logger
from common.GetMeetingInfo import GetMeetingInfo,GetDetailedInformation
from common.GetMeetingInfo import MeetingLoginApi,GetMeetingInfoApi,LoginApiParams,GetInfoApiParams,Headers
from common.SetInfoToExcel import SetInfoToExcel

if __name__ == "__main__":
    #判断是否有会议召开
    MeetingApi = GetMeetingInfo(MeetingLoginApi, LoginApiParams, Headers)
    MeetingApi.Login()
    MeetingApi = GetMeetingInfo(GetMeetingInfoApi, GetInfoApiParams, Headers)
    MeetingInfoDict = MeetingApi.GetInfo()
    if "items" in MeetingInfoDict.keys():
        #将所有信息写入到excel中
        SetInfoToExcel()
        logger().info("会议日报写入excel完成")
    else:
        logger().info("该时间段内没有会议召开")