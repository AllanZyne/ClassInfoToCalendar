# coding: utf-8
#!/usr/bin/python

import sys
import time, datetime
import json
from random import Random

class CheckType:
	checkFirstWeekDate = 0
	checkReminder = 1

YES = 0
NO = 1

DONE_firstWeekDate = time.time()
DONE_reminder = ""
DONE_EventUID = ""
DONE_UnitUID = ""
DONE_CreatedTime = ""
DONE_ALARMUID = ""

classTimeList = []
classInfoList = []

# compatible
raw_input = input

def main():
	basicSetting();
	uniteSetting();
	classInfoHandle();
	icsCreateAndSave();

def save(string):
     f = open("class.ics", 'wb')
     f.write(string.encode("utf-8"))
     f.close()

def icsCreateAndSave():
	with open('conf_classTime.json', 'r') as f:
		data = json.load(f)

	icsString = "BEGIN:VCALENDAR\nMETHOD:PUBLISH\nVERSION:2.0"
	icsString = icsString + "\nX-WR-CALNAME:" + data["calendarName"]
	icsString = icsString + "\nPRODID:-//Apple Inc.//Mac OS X 10.12//EN"
	icsString = icsString + "\nX-WR-TIMEZONE:Asia/Shanghai"
	icsString = icsString + "\nCALSCALE:GREGORIAN"
	icsString = icsString + "\nBEGIN:VTIMEZONE"
	icsString = icsString + "\nTZID:Asia/Shanghai"
	icsString = icsString + "\nBEGIN:STANDARD"
	icsString = icsString + "\nTZOFFSETFROM:+0800"
	icsString = icsString + "\nDTSTART:19890917T000000"
	icsString = icsString + "\nTZNAME:GMT+8"
	icsString = icsString + "\nTZOFFSETTO:+0800"
	icsString = icsString + "\nEND:STANDARD"
	icsString = icsString + "\nEND:VTIMEZONE\n"

	global classTimeList, DONE_ALARMUID, DONE_UnitUID
	eventString = ""
	for classInfo in classInfoList :
		i = int(classInfo["classTime"]-1)
		className = classInfo["className"]
		endTime = classTimeList[i]["endTime"]
		startTime = classTimeList[i]["startTime"]
		LOCATION = classInfo["classroom"]

		index = 0
		for date in classInfo["date"]:
			eventString = eventString + "BEGIN:VEVENT"
			eventString = eventString + "\nCREATED:"+classInfo["CREATED"]
			eventString = eventString + "\nUID:"+classInfo["UID"][index]
			eventString = eventString + "\nDTEND;TZID=Asia/Shanghai:"+date+"T"+endTime+"00"
			eventString = eventString + "\nTRANSP:OPAQUE"
			eventString = eventString + "\nX-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC"
			eventString = eventString + "\nSUMMARY:"+className
			eventString = eventString + "\nDTSTART;TZID=Asia/Shanghai:"+date+"T"+startTime+"00"
			eventString = eventString + "\nDTSTAMP:"+DONE_CreatedTime
			eventString = eventString + "\nSEQUENCE:0"
			# BEGIN ALARM
			eventString = eventString + "\nBEGIN:VALARM"
			eventString = eventString + "\nX-WR-ALARMUID:"+DONE_ALARMUID
			eventString = eventString + "\nUID:"+DONE_UnitUID
			eventString = eventString + "\nTRIGGER:"+DONE_reminder
			eventString = eventString + "\nDESCRIPTION:事件提醒"
			eventString = eventString + "\nACTION:DISPLAY"
			eventString = eventString + "\nEND:VALARM"
			# END ALARM
			eventString = eventString + "\nLOCATION:"+LOCATION
			eventString = eventString + "\nEND:VEVENT\n"
			index += 1

	for week in range(int(data["totalWeek"])):
		startDate = datetime.datetime.fromtimestamp(int(time.mktime(DONE_firstWeekDate))) + datetime.timedelta(weeks = week)
		date = startDate.strftime('%Y%m%d')

		eventString = eventString + "BEGIN:VEVENT"
		eventString = eventString + "\nCREATED:"+DONE_CreatedTime
		eventString = eventString + "\nUID:"+UID_Create()
		eventString = eventString + "\nDTEND;VALUE=DATE;TZID=Asia/Shanghai:"+date
		eventString = eventString + "\nTRANSP:TRANSPARENT"
		eventString = eventString + "\nX-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC"
		eventString = eventString + "\nSUMMARY:" + "第 {} 周".format(week+1)
		eventString = eventString + "\nDTSTART;VALUE=DATE;TZID=Asia/Shanghai:"+date
		eventString = eventString + "\nDTSTAMP:"+DONE_CreatedTime
		eventString = eventString + "\nSEQUENCE:0"
		eventString = eventString + "\nEND:VEVENT\n"

	icsString = icsString + eventString + "END:VCALENDAR"
	save(icsString)
	print("icsCreateAndSave")

def classInfoHandle():
	global classInfoList
	global DONE_firstWeekDate
	i = 0

	for classInfo in classInfoList :
		# 具体日期计算出来
		startWeek = json.dumps(classInfo["week"]["startWeek"])
		endWeek = json.dumps(classInfo["week"]["endWeek"])
		weekday = float(json.dumps(classInfo["weekday"]))

		dateLength = float((int(startWeek) - 1) * 7)
		startDate = datetime.datetime.fromtimestamp(int(time.mktime(DONE_firstWeekDate))) + datetime.timedelta(days = dateLength + weekday - 1)
		string = startDate.strftime('%Y%m%d')

		dateLength = float((int(endWeek) - 1) * 7)
		endDate = datetime.datetime.fromtimestamp(int(time.mktime(DONE_firstWeekDate))) + datetime.timedelta(days = dateLength + weekday - 1)

		date = startDate
		dateList = []
		dateList.append(string)
		i = NO
		while (i):
			date = date + datetime.timedelta(days = 7.0)
			if(date > endDate):
				i = YES
			else:
				string = date.strftime('%Y%m%d')
				dateList.append(string)
		classInfo["date"] = dateList

		# 设置 UID
		CreateTime()
		classInfo["CREATED"] = DONE_CreatedTime
		classInfo["DTSTAMP"] = DONE_CreatedTime
		UID_List = []
		for date  in dateList:
			UID_List.append(UID_Create())
		classInfo["UID"] = UID_List
	print("classInfoHandle")

def UID_Create():
	return random_str(20) + "&Chanjh.com"

def CreateTime():
	# 生成 CREATED
	global DONE_CreatedTime
	date = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
	DONE_CreatedTime = date + "Z"
	# 生成 UID
	# global DONE_EventUID
	# DONE_EventUID = random_str(20) + "&Chanjh.com"

	print("CreateTime")

def uniteSetting():
	#
	global DONE_ALARMUID
	DONE_ALARMUID = random_str(30) + "&Chanjh.com"
	#
	global DONE_UnitUID
	DONE_UnitUID = random_str(20) + "&Chanjh.com"
	print("uniteSetting")

def setClassTime():
	data = []
	with open('conf_classTime.json', 'r') as f:
		data = json.load(f)
	global classTimeList
	classTimeList = data["classTime"]
	print("setclassTime")

def setClassInfo():
	data = []
	with open('conf_classInfo.json', 'r') as f:
		data = json.load(f)
	global classInfoList
	classInfoList = data["classInfo"]
	print("setClassInfo:")

def setFirstWeekDate(firstWeekDate):
	global DONE_firstWeekDate
	DONE_firstWeekDate = time.strptime(firstWeekDate,'%Y%m%d')
	print("setFirstWeekDate:",DONE_firstWeekDate)

def setReminder(reminder):
	global DONE_reminder
	reminderList = ["-PT20M","-PT30M","-PT1H","-PT2H","-P1D"]
	if(reminder == "1"):
		DONE_reminder = reminderList[0]
	elif(reminder == "2"):
		DONE_reminder = reminderList[1]
	elif(reminder == "3"):
		DONE_reminder = reminderList[2]
	elif(reminder == "4"):
		DONE_reminder = reminderList[3]
	elif(reminder == "5"):
		DONE_reminder = reminderList[4]
	else:
		DONE_reminder = "NULL"

	print("setReminder",reminder)

def checkReminder(reminder):
	print("checkReminder:",reminder)
	List = ["0","1","2","3","4","5"]
	for num in List:
		if (reminder == num):
			return YES
	return NO

def checkFirstWeekDate(firstWeekDate):
	# 长度判断
	if(len(firstWeekDate) != 8):
		return NO;

	year = firstWeekDate[0:4]
	month = firstWeekDate[4:6]
	date = firstWeekDate[6:8]
	dateList = [31,29,31,30,31,30,31,31,30,31,30,31]

	# 年份判断
	if(int(year) < 1970):
		return NO
	# 月份判断
	if(int(month) == 0 or int(month) > 12):
		return NO;
	# 日期判断
	if(int(date) > dateList[int(month)-1]):
		return NO;

	print("checkFirstWeekDate:",firstWeekDate)
	return YES

def basicSetting():
	with open('conf_classTime.json', 'r') as f:
		data = json.load(f)
	
	firstWeekDate = data["firstWeekDate"]
	checkInput(CheckType.checkFirstWeekDate, firstWeekDate)

	info = "正在配置上课时间信息……\n"
	print(info)
	try :
		setClassTime()
		print("配置上课时间信息完成。\n")
	except :
		sys_exit()

	info = "正在配置课堂信息……\n"
	print(info)
	try :
		setClassInfo()
		print("配置课堂信息完成。\n")
	except :
		sys_exit()

	info = "正在配置提醒功能，请输入数字选择提醒时间\n【0】不提醒\n【1】上课前 20 分钟提醒\n【2】上课前 30 分钟提醒\n【3】上课前 1 小时提醒\n【4】上课前 2 小时提醒\n【5】上课前 1 天提醒\n"
	reminder = raw_input(info)
	checkInput(CheckType.checkReminder, reminder)

def checkInput(checkType, input):
	if(checkType == CheckType.checkFirstWeekDate):
		if (checkFirstWeekDate(input)):
			info = "输入有误，请重新输入第一周的星期一日期(如：20170904):\n"
			firstWeekDate = raw_input(info)
			checkInput(CheckType.checkFirstWeekDate, firstWeekDate)
		else:
			setFirstWeekDate(input)
	elif(checkType == CheckType.checkReminder):
		if(checkReminder(input)):
			info = "输入有误，请重新输入\n【1】上课前 20 分钟提醒\n【2】上课前 30 分钟提醒\n【3】上课前 1 小时提醒\n【4】上课前 2 小时提醒\n【5】上课前 1 天提醒\n"
			reminder = raw_input(info)
			checkInput(CheckType.checkReminder, reminder)
		else:
			setReminder(input)
	else:
		print("程序出错")
		end

def random_str(randomlength):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def sys_exit():
	print("配置文件错误，请检查。\n")
	sys.exit()


main()
