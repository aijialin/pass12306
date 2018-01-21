import time, datetime


def get(city):
	station_names = ""
	code = ""
	with open("cityCode.data", "r", encoding='utf-8') as f:
		station_names = f.read()
	for i in station_names.split('@'):
		if i:
			tmp = i.split('|')
			if tmp[1] == city:
				return tmp[2]
			

def trans(arr):
	ret = ""
	coordinate_dic = {
		1:"35,30", 2:"100,35", 3:"175,35", 4:"255,35",
	  	5:"35,120",6:"100,125",7:"176,128",8:"256,129",
	}
	for i in reversed(arr):
		ret += coordinate_dic[int(i)] + ','
	
	return ret[0:-1]

def trans_date(date):
	#ret = "Tue Feb 13 2018 00:00:00 GMT+0800 (中国标准时间)"
	d = [int(i) for i in date.split('-')]
	dateC = datetime.datetime(d[0],d[1],d[2],0,0,0)
	timestamp = time.mktime(dateC.timetuple())
	dd = time.asctime(time.localtime(timestamp)).split(' ')
	ret = "%s %s %s %s %s %s %s" % (dd[0], dd[1], dd[2], dd[4], dd[3], "GMT+0800", "(中国标准时间)")
	return ret



