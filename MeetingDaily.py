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
from common.GetMeetingInfo import meeting_switch,user_switch
from common.SetInfoToExcel import SetInfoToExcel,SetNubeInfoToExcel

if __name__ == "__main__":

    if meeting_switch == 1:
        #判断是否有会议召开
        MeetingApi = GetMeetingInfo(MeetingLoginApi, LoginApiParams, Headers)
        MeetingApi.Login()
        MeetingApi = GetMeetingInfo(GetMeetingInfoApi, GetInfoApiParams, Headers)
        MeetingInfoDict = MeetingApi.GetInfo()
        if "items" in MeetingInfoDict.keys():
            print "时间范围内有商业用户进行开会".encode("GBK")
            logger().info("时间范围内有商业用户进行开会")
            #将所有信息写入到excel中
            SetInfoToExcel()
            print "会议日报全部写入到excel"
            logger().info("会议日报全部写入到excel")
        else:
            print "该时间段内没有会议召开".encode("GBK")
            logger().error("该时间段内没有会议召开")
    else:
        print "商业用户会议报表输出关闭".encode("GBK")
        logger().error("商业用户会议报表输出关闭")

    if user_switch == 1:
        # 将用户的会议信息写入到excel中
        SetNubeInfoToExcel()
        print "按照用户筛选的日报写入excel完成".encode("GBK")
        logger().info("按照用户筛选的日报写入excel完成")
    else:
        print "按用户筛选的报表输出关闭".encode("GBK")
        logger().error("按用户筛选的报表输出关闭")


