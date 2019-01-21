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
import sys
#解决python的str默认是ascii编码，和unicode编码冲突
reload(sys)
sys.setdefaultencoding('utf8')
#导入自定义的模块
from common.GetMeetingInfo import GetMeetingInfo,GetDetailedInformation
from common.GetMeetingInfo import GetMeetingInfoApi,GetInfoApiParams,LoginApiParams,MeetingLoginApi,Headers,GetUserInfoApi
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
                response = urllib2.urlopen(request,timeout=30)
                response_result = response.read()
                response_dict = json.loads(response_result)
                for i in response_dict["users"]:
                    if "nickName" in i.keys():
                        nickName = i["nickName"]
                    else:
                        nickName = "未命名"
                    UserNameInfoListTemp.append({User: nickName})
            else:
                continue
        UserNameInfoList.append(UserNameInfoListTemp)
        UserNameInfoListTemp = []

    return UserNameInfoList

#获取视频号对应的设备类型
def GetUserDeviceType():

    DeviceTypeInfoListTemp = []
    DeviceTypeInfoList = []
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
                UserParams = {"service": "searchAccount", "params": {"nubeNumbers": [User]}}
                UserStr = urllib.urlencode(UserParams)
                NewUrl = GetUserInfoApi + "?" + UserStr
                request = urllib2.Request(url=NewUrl, headers=Headers)
                response = urllib2.urlopen(request,timeout=30)
                response_result = response.read()
                response_dict = json.loads(response_result)
                DeviceType = response_dict["users"][0]["deviceType"]
                DeviceTypeInfoListTemp.append({User: DeviceType})
            else:
                continue
        DeviceTypeInfoList.append(DeviceTypeInfoListTemp)
        DeviceTypeInfoListTemp = []

    return DeviceTypeInfoList

#共同获取用户名和设备类型
def GetUserAll():
    UserNameInfoListTemp = []
    UserNameInfoList = []
    UserDeviceTypeInfoListTemp = []
    UserDeviceTypeInfoList = []
    MeetingApi = GetMeetingInfo(MeetingLoginApi, LoginApiParams, Headers)
    MeetingApi.Login()
    MeetingApi = GetMeetingInfo(GetMeetingInfoApi, GetInfoApiParams, Headers)
    MeetingApi.GetInfo()
    UserAlllist = GetDetailedInformation(MeetingApi.GetInfo())
    UserAllAvailableList = UserAlllist.AvailableMeetingList()
    for item in range(len(UserAllAvailableList)):
        UserIdList = UserAllAvailableList[item]["userIdList"]
        for item in range(len(UserIdList)):
            User = UserIdList[item]
            User = User.encode("utf-8")
            if len(User) == 8:
                UserParams = {"service": "searchAccount", "params": {"nubeNumbers": [User]}}
                UserStr = urllib.urlencode(UserParams)
                NewUrl = GetUserInfoApi + "?" + UserStr
                request = urllib2.Request(url=NewUrl, headers=Headers)
                response = urllib2.urlopen(request, timeout=30)
                response_result = response.read()
                response_dict = json.loads(response_result)
                for i in response_dict["users"]:
                    if "nickName" in i.keys():
                        nickName = i["nickName"]
                    else:
                        nickName = "未命名"
                DeviceType = response_dict["users"][0]["deviceType"]
                UserNameInfo = "%s-%s" % (User,nickName)
                DeviceTypeInfo = "%s-%s" % (User,DeviceType)
                UserNameInfoListTemp.append(UserNameInfo)
                UserDeviceTypeInfoListTemp.append(DeviceTypeInfo)
            else:
                continue
        UserNameInfoList.append(UserNameInfoListTemp)
        UserNameInfoListTemp = []
        UserDeviceTypeInfoList.append(UserDeviceTypeInfoListTemp)
        UserDeviceTypeInfoListTemp = []

    return (UserNameInfoList,UserDeviceTypeInfoList)
