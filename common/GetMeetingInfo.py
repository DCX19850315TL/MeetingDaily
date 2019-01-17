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

    #只有2人及以上的会议才在日报中体现
    def AvailableMeetingList(self):
        AvailableMeetingList = []
        for item in range(len(self.MeetingInfo["items"])):
            userCount = self.MeetingInfo["items"][item]["userCount"]
            if userCount == 1:
                continue
            else:
                AvailableMeetingList.append(self.MeetingInfo["items"][item])

        return AvailableMeetingList

    #计算列表的个数
    def List_len(self):

        return len(self.AvailableMeetingList())

    #会议号的信息
    def GetMeetingNumber(self):
        MeetingNumberList = []
        for item in range(self.List_len()):
            MeetingNumber = self.AvailableMeetingList()[item]["meetingId"]
            MeetingNumberList.append(MeetingNumber)

        return MeetingNumberList

    #会议几点开始的时间
    def GetMeetingTime(self):
        MeetingTimeList = []
        for item in range(self.List_len()):
            MeetingTime = self.AvailableMeetingList()[item]["timeStamps"]
            MeetingTimeList.append(MeetingTime)

        return MeetingTimeList

    #会议持续了多长时间
    def GetMeetingDuration(self):
        MeetingDurationList = []
        for item in range(self.List_len()):
            MeetingDuration = self.AvailableMeetingList()[item]["duration"]
            MeetingDurationList.append(MeetingDuration)

        return MeetingDurationList

    #端到端总体合格率
    def GetPtoPTotal(self):
        isQualifiedSum = 0
        isQualifiedCountList = []
        PtoPTotalQualifiedPercentList = []
        for item in range(self.List_len()):
            isQualified = self.AvailableMeetingList()[item]["c2cquality"]
            isQualifiedstr = isQualified.encode("utf-8")
            isQualifiedList = isQualified.split("|")
            for item in range(len(isQualifiedList)):
                isQualifiedList2 = isQualifiedList[item].split("/")
                isQualifiedCountList.append(isQualifiedList2)
            for item in range(len(isQualifiedList)):
                Qualified = int(isQualifiedCountList[item][2])
                if Qualified == 1:
                    isQualifiedSum+=1
            PtoPTotal = len(isQualifiedList)
            PtoPTotalQualifiedPercent = str(isQualifiedSum / PtoPTotal * 100) + "%"
            PtoPTotalQualifiedPercentList.append(PtoPTotalQualifiedPercent)

        return PtoPTotalQualifiedPercentList

    #丢包平均合格率
    def PacketLossAverage(self):
        PacketLossSum = 0
        isQualifiedCountList = []
        PacketLossAverageList = []
        for item in range(self.List_len()):
            isQualified = self.AvailableMeetingList()[item]["c2cquality"]
            isQualifiedstr = isQualified.encode("utf-8")
            isQualifiedList = isQualified.split("|")
            for item in range(len(isQualifiedList)):
                isQualifiedList2 = isQualifiedList[item].split("/")
                isQualifiedCountList.append(isQualifiedList2)
            for item in range(len(isQualifiedList)):
                PacketLoss = int(isQualifiedCountList[item][3])
                PacketLossSum+=PacketLoss
            PacketLossCount = len(isQualifiedList) * 100
            PacketLossAverage = str(int(float(PacketLossSum) / float(PacketLossCount) * 100)) + "%"
            PacketLossAverageList.append(PacketLossAverage)

        return PacketLossAverageList

    #空音包平均合格率
    def SoundPacketLossAverage(self):
        SoundPacketLossSum = 0
        isQualifiedCountList = []
        SoundPacketLossAverageList = []
        for item in range(self.List_len()):
            isQualified = self.AvailableMeetingList()[item]["c2cquality"]
            isQualifiedstr = isQualified.encode("utf-8")
            isQualifiedList = isQualified.split("|")
            for item in range(len(isQualifiedList)):
                isQualifiedList2 = isQualifiedList[item].split("/")
                isQualifiedCountList.append(isQualifiedList2)
            for item in range(len(isQualifiedList)):
                SoundPacketLoss = int(isQualifiedCountList[item][5])
                SoundPacketLossSum += SoundPacketLoss
            SoundPacketLossCount = len(isQualifiedList) * 100
            SoundPacketLossAverage = str(int(float(SoundPacketLossSum) / float(SoundPacketLossCount) * 100)) + "%"
            SoundPacketLossAverageList.append(SoundPacketLossAverage)

        return SoundPacketLossAverageList

    #丢包最高合格率
    def PacketLossMax(self):
        isQualifiedCountList = []
        PacketLossTempList = []
        PacketLossMaxList = []
        for item in range(self.List_len()):
            isQualified = self.AvailableMeetingList()[item]["c2cquality"]
            isQualifiedstr = isQualified.encode("utf-8")
            isQualifiedList = isQualified.split("|")
            for item in range(len(isQualifiedList)):
                isQualifiedList2 = isQualifiedList[item].split("/")
                isQualifiedCountList.append(isQualifiedList2)
            for item in range(len(isQualifiedList)):
                PacketLoss = int(isQualifiedCountList[item][3])
                PacketLossTempList.append(PacketLoss)
            PacketLossMax = str(max(PacketLossTempList)) + "%"
            PacketLossMaxList.append(PacketLossMax)

        return PacketLossMaxList

    #空音包最高合格率
    def SoundPacketLossMax(self):
        isQualifiedCountList = []
        SoundPacketLossTempList = []
        SoundPacketLossMaxList = []
        for item in range(self.List_len()):
            isQualified = self.AvailableMeetingList()[item]["c2cquality"]
            isQualifiedstr = isQualified.encode("utf-8")
            isQualifiedList = isQualified.split("|")
            for item in range(len(isQualifiedList)):
                isQualifiedList2 = isQualifiedList[item].split("/")
                isQualifiedCountList.append(isQualifiedList2)
            for item in range(len(isQualifiedList)):
                SoundPacketLoss = int(isQualifiedCountList[item][5])
                SoundPacketLossTempList.append(SoundPacketLoss)
            SoundPacketLossMax = str(max(SoundPacketLossTempList)) + "%"
            SoundPacketLossMaxList.append(SoundPacketLossMax)

        return SoundPacketLossMaxList

    #丢包最低合格率
    def PacketLossMin(self):
        isQualifiedCountList = []
        PacketLossTempList = []
        PacketLossMinList = []
        for item in range(self.List_len()):
            isQualified = self.AvailableMeetingList()[item]["c2cquality"]
            isQualifiedstr = isQualified.encode("utf-8")
            isQualifiedList = isQualified.split("|")
            for item in range(len(isQualifiedList)):
                isQualifiedList2 = isQualifiedList[item].split("/")
                isQualifiedCountList.append(isQualifiedList2)
            for item in range(len(isQualifiedList)):
                PacketLoss = int(isQualifiedCountList[item][3])
                PacketLossTempList.append(PacketLoss)
            PacketLossMin = str(min(PacketLossTempList)) + "%"
            PacketLossMinList.append(PacketLossMin)

        return PacketLossMinList

    #空音包最低合格率
    def SoundPacketLossMin(self):
        isQualifiedCountList = []
        SoundPacketLossTempList = []
        SoundPacketLossMinList = []
        for item in range(self.List_len()):
            isQualified = self.AvailableMeetingList()[item]["c2cquality"]
            isQualifiedstr = isQualified.encode("utf-8")
            isQualifiedList = isQualified.split("|")
            for item in range(len(isQualifiedList)):
                isQualifiedList2 = isQualifiedList[item].split("/")
                isQualifiedCountList.append(isQualifiedList2)
            for item in range(len(isQualifiedList)):
                SoundPacketLoss = int(isQualifiedCountList[item][5])
                SoundPacketLossTempList.append(SoundPacketLoss)
            SoundPacketLossMin = str(min(SoundPacketLossTempList)) + "%"
            SoundPacketLossMinList.append(SoundPacketLossMin)

        return SoundPacketLossMinList

    #不合格端到端明细数据
    def DetailData(self):
        isQualifiedCountList = []
        DetailDataTempList = []
        DetailDataList = []
        for item in range(self.List_len()):
            isQualified = self.AvailableMeetingList()[item]["c2cquality"]
            isQualifiedstr = isQualified.encode("utf-8")
            isQualifiedList = isQualified.split("|")
            for item in range(len(isQualifiedList)):
                isQualifiedList2 = isQualifiedList[item].split("/")
                isQualifiedCountList.append(isQualifiedList2)
            for item in range(len(isQualifiedList)):
                MainCaller = isQualifiedCountList[item][0].encode("utf-8")
                BackupCaller = isQualifiedCountList[item][1].encode("utf-8")
                Qualified = int(isQualifiedCountList[item][2])
                PacketLoss = str(isQualifiedCountList[item][3]) + "%"
                SoundPacketLoss = str(isQualifiedCountList[item][5]) + "%"
                if Qualified == 1:
                    QualifiedName = "合格"
                else:
                    QualifiedName = "不合格"
                DetailDataName = MainCaller + "->" + BackupCaller + "|" + QualifiedName + "|" + PacketLoss + "|" + SoundPacketLoss
                DetailDataTempList.append(DetailDataName)
            DetailDataList.append(DetailDataTempList)

    #开会人数
    def MeetingPeopleNumber(self):
        MeetingPeopleNumberTempList = []
        MeetingPeopleNumberList = []
        for item in range(self.List_len()):
            MeetingPeopleNumber = self.AvailableMeetingList()[item]["userIdList"]
            for item in range(len(MeetingPeopleNumber)):
                MeetingPeople = MeetingPeopleNumber[item]
                MeetingPeopleStr = MeetingPeople.encode("utf-8")
                if len(MeetingPeopleStr) == 8:
                    MeetingPeopleNumberTempList.append(MeetingPeopleStr)
                else:
                    continue
            MeetingPeopelNumberTemp = len(MeetingPeopleNumberTempList)
            MeetingPeopleNumberList.append(MeetingPeopelNumberTemp)

        return MeetingPeopleNumberList

a = GetDetailedInformation(MeetingApi.GetInfo())
a.AvailableMeetingList()
a.List_len()
a.GetPtoPTotal()
a.PacketLossAverage()
a.SoundPacketLossAverage()
a.PacketLossMax()
a.SoundPacketLossMax()
a.PacketLossMin()
a.SoundPacketLossMin()
a.MeetingPeopleNumber()
a.DetailData()