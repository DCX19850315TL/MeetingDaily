#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
@author: tanglei
@contact: tanglei_0315@163.com
@file: GetUserInfo.py
@time: 2019/1/14 11:26
'''
#导入系统模块
import urllib
import urllib2
import json
#导入自定义的模块
from common.GetMeetingInfo import GetMeetingInfoApi,GetInfoApiParams,Headers,GetUserInfoApi
from common.GetMeetingInfo import GetMeetingInfo,GetDetailedInformation
from common.logger import logger

#获取视频号对应的用户名
def GetUserNameInfo():

    UserNameInfoListTemp = []
    UserNameInfoList = []
    MeetingApi = GetMeetingInfo(GetMeetingInfoApi, GetInfoApiParams, Headers)
    MeetingApi.GetInfo()
    Userlist = GetDetailedInformation(MeetingApi.GetInfo())
    UserAvailableList = Userlist.AvailableMeetingList()
    for item in range(len(UserAvailableList)):
        UserIdList = UserAvailableList[item]["userIdList"]
        for item in range(len(UserIdList)):
            User = UserIdList[item]
            User = User.encode("utf-8")
            if len(User) == 8:
                UserParams = {"service":"searchAccount","params":{"nubeNumbers":[User]}}
                UserStr = urllib.urlencode(UserParams)
                NewUrl = GetUserInfoApi + "?" + UserStr
                request = urllib2.Request(url=NewUrl,headers=Headers)
                response = urllib2.urlopen(request)
                response_result = response.read()
                response_dict = json.loads(response_result)
                nickName = response_dict["users"][0]["nickName"]
                UserNameInfoListTemp.append({User:nickName})
            else:
                continue
        UserNameInfoList.append(UserNameInfoListTemp)
        print UserNameInfoList
        return UserNameInfoList


#获取视频号对应的设备类型

GetUserNameInfo()