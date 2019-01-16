#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
@author: tanglei
@contact: tanglei_0315@163.com
@file: GetMeetingInfo.py
@time: 2019/1/14 11:26
'''
#导入系统模块
import os
import sys
import ConfigParser
import urllib
import urllib2
import cookielib
import json
import traceback
#导入自定义模块
from common.logger import logger

#设置配置文件
path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
seeting_file = os.path.join(path,'conf\seeting.ini')
conf = ConfigParser.ConfigParser()
conf.read(seeting_file)
#设置全局变量
#起始时间
starttime = conf.get("time","starttime")
#结束时间
endtime = conf.get("time","endtime")
#会议分析登陆接口
MeetingLoginApi = conf.get("api","MeetingLogin")
#会议分析获取会议信息接口
GetMeetingInfoApi = conf.get("api","GetMeetingInfo")
#会议类型
MeetingType = conf.get("entName","type")
#企业用户中心获取视频号信息接口
GetUserInfoApi = conf.get("api","GetUserInfo")
#POST请求头的信息
Headers = {"Content-type": "application/x-www-form-urlencoded","X-Requested-With":"XMLHttpRequest"}

#根据配置文件获取指定时间点的会议信息
class GetMeetingInfo(object):

    def __init__(self,url,params,headers):

        self.Url = url
        self.Params = params
        self.Headers = headers

    def Login(self):
        try:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            request = urllib2.Request(url=self.Url,data=self.Params,headers=self.Headers)
            response = urllib2.urlopen(request,timeout=30)
        except:
            s = traceback.format_exc()
            logger().error(s)

    def GetInfo(self):
        try:
            request = urllib2.Request(url=self.Url,data=self.Params,headers=self.Headers)
            response = urllib2.urlopen(request, timeout=30)
            response_result = response.read()
            response_dict = json.loads(response_result)
            print response_dict
            return response_dict
        except:
            s = traceback.format_exc()
            logger().error(s)

LoginApiParams = urllib.urlencode({"username":"admin","userpwd":"654321"})
MeetingApi = GetMeetingInfo(MeetingLoginApi,LoginApiParams,Headers)
MeetingApi.Login()
GetInfoApiParams = urllib.urlencode({"userId":"","meetingId":"","relayId":"","startTime":starttime,"endTime":endtime,"currPage":1,"directionType":"undefined","companyName":MeetingType})
MeetingApi = GetMeetingInfo(GetMeetingInfoApi,GetInfoApiParams,Headers)
MeetingApi.GetInfo()

class GetDetailedInformation(object):

    def __init__(self,MeetingInfo):

        self.MeetingInfo = MeetingInfo

    def List_len(self):

        return len(self.MeetingInfo["items"])

    def GetMeetingNumber(self):
        MeetingNumberList = []
        for item in range(self.List_len()):
            MeetingNumber = self.MeetingInfo["items"][item]["meetingId"]
            MeetingNumberList.append(MeetingNumber)

        return MeetingNumberList

    def GetMeetingTime(self):
        MeetingTimeList = []
        for item in range(self.List_len()):
            MeetingTime = self.MeetingInfo["items"][item]["timeStamps"]
            MeetingTimeList.append(MeetingTime)

        return MeetingTimeList

    def GetMeetingDuration(self):
        MeetingDurationList = []
        for item in range(self.List_len()):
            MeetingDuration = self.MeetingInfo["items"][item]["duration"]
            MeetingDurationList.append(MeetingDuration)

        return MeetingDurationList

a = GetDetailedInformation(MeetingApi.GetInfo())
a.GetMeetingNumber()