#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, requests, os
import time, re

import config, utils, send_email

import urllib.parse
from log import Logger


# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class req():
	def __init__(self):
		self.s = requests.Session()
		self.headers = config.headers
		self.timeout = config.timeout
		self.s.verify = False
		self.max_retry_times = 30

		self.jar = requests.cookies.RequestsCookieJar()
		self.jar.set("RAIL_EXPIRATION", config.cookies["RAIL_EXPIRATION"], domain="12306.cn", path='/')
		self.jar.set("RAIL_DEVICEID", config.cookies["RAIL_DEVICEID"], domain="12306.cn", path='/')

	def get(self, url, params=None):
		Logger.info("正在访问 [%s]" % url)
		count = 1
		while True:
			ret = self.s.get(url, params=params, headers=self.headers, cookies=self.jar, timeout=self.timeout)
			if ret.url != config.URL["err_url"]:
				return ret
			time.sleep(1)
			Logger.info("重新访问 [%s] %d 次" % (url, count)) 
			count += 1
			if count > self.max_retry_times:
				Logger.info("访问 [%s] 出错" % url)
				return ret

	def post(self, url, data=None):
		Logger.info("正在访问 [%s]" % url)
		count = 1
		while True:
			ret = self.s.post(url, data=data, headers=self.headers, cookies=self.jar, timeout=self.timeout)
			if ret.url != config.URL["err_url"]:
				return ret
			time.sleep(1)
			Logger.info("重新访问 [%s] %d 次" % (url, count)) 
			count += 1
			if count > self.max_retry_times:
				Logger.info("访问 [%s] 出错" % url)
				return ret


class pass12306():
	def __init__(self):
		self.s = req()
		self.max_retry_times = 4
		
	def login(self):
		ret = {
			"result_code"		: 0,
			"result_message"	: "",
		}
		r0 = self.s.get(config.URL["login_init"]) #获取请求cookie
		if r0.url == config.URL["err_url"]:
			Logger.info("程序开始,初始化请求环境失败")
			ret["result_code"] = -1
			ret["result_message"] = "初始化请求环境失败"
			return ret

		Logger.info("程序开始,访问%s, 初始化请求环境成功" % r0.url)
		#print (r.text)

		#检测用户登陆状态
		r = self.s.post(config.URL["check_url"], data={"appid":"otn"})
		try:
			if r.json()["result_code"] != 1: # 已经登陆
				ret["result_code"] = -2
				ret["result_message"] = r.json()["result_message"]
				Logger.info("%s" % ret["result_message"])
				return ret
			else:
				Logger.info("%s" % r.text)
		except:
			Logger.info("检测用户登陆状态失败")
			ret["result_code"] = -2
			ret["result_message"] = "检测用户登陆状态失败"
			return ret
		
		#如果未登陆，获取验证码
		r1 = self.s.get(config.URL["captcha"])
		try:
			with open(config.yzmpath, 'wb') as f:
				f.write(r1.content)
			os.startfile(config.yzmpath)
			Logger.info("获取验证码成功")
		except:
			Logger.info("获取验证码失败")
			ret["result_code"] = -3
			ret["result_message"] = "获取验证码失败"
			return ret
		print (
		'''
		#=======================================================================
        # 根据打开的图片识别验证码后手动输入，输入正确验证码对应的位置，例如：2,5
        # ---------------------------------------
        #         |         |         |
        #    1    |    2    |    3    |     4
        #         |         |         |
        # ---------------------------------------
        #         |         |         |
        #    5    |    6    |    7    |     8
        #         |         |         |
        # ---------------------------------------
        #=======================================================================
        '''
		)
		code = input("请输入验证码对应的编号：")

		while code == "refresh":
			r1 = self.s.get(config.URL["captcha"])
			with open(config.yzmpath, 'wb') as f:
				f.write(r1.content)
			os.startfile(config.yzmpath)
			code = input("please enter code:")
			
		code = code.split(',')
		code = utils.trans(code)
			
		params2 = {
			"answer": code,
	        "login_site": "E",
	        "rand": "sjrand"
		}
		#验证码校验 
		r2 = self.s.post(config.URL["captcha_check"], data=params2)
		try:
			if r2.json()["result_code"] != "4":
				ret["result_code"] = -4 #验证码错误
				ret["result_message"] = r2.json()["result_message"]
				Logger.info("%s" % ret["result_message"])
				return ret
			else:
				Logger.info("验证码校验成功")
		except:
			Logger.info("验证码校验失败")
			ret["result_code"] = -4
			ret["result_message"] = "验证码校验失败"
			return ret

		#验证登陆
		params3 = {
			"username": config.username,
	        "password": config.password,
	        "appid": "otn"
		}
		r3 = self.s.post(config.URL["login"], data=params3)
		try:
			if json.loads(r3.text)["result_code"] != 0:
				ret["result_code"] = -5 #登录失败
				ret["result_message"] = json.loads(r3.text)["result_message"]
				Logger.info("%s" % ret["result_message"])
				return ret
			else:
				Logger.info("%s" % json.loads(r3.text)["result_message"])
		except:
			ret["result_code"] = -5
			ret["result_message"] = "登录失败"
			Logger.info("[5]登录失败")
			return ret

		#检测用户登陆状态
		r4 = self.s.post(config.URL["check_url"], data={"appid":"otn"})
		try:
			r4_list = json.loads(r4.text)
			if r4_list["result_code"] != 0:
				ret["result_code"] = -6 #登录失败
				ret["result_message"] = r4_list["result_message"]
				return ret
			else:
				Logger.info("%s" % r4_list["result_message"])
		except:
			ret["result_code"] = -6
			ret["result_message"] = "检测用户登陆状态失败"
			Logger.info("检测用户登陆状态失败")
			return ret
		
		r5 = self.s.post(config.URL["uamauthclient"], data={"tk":r4_list["newapptk"]})
		try:
			if json.loads(r5.text)["result_code"] != 0:
				ret["result_code"] = -7
				ret["result_message"] = json.loads(r5.text)["result_message"]
				Logger.info("%s" % json.loads(r5.text)["result_message"])
				return ret
			else:	
				ret["result_code"] = 0
				ret["result_message"] = json.loads(r5.text)["result_message"]
				ret["username"] = json.loads(r5.text)["username"]
				return ret
		except:
			ret["result_code"] = -7
			ret["result_message"] = "uamauthclient状态失败"
			Logger.info("uamauthclient状态失败")
			return ret

	def monitor(self):
		ret = {
			"result_code"		: 0,
			"result_message"	: "",
		}
		params = {
			"leftTicketDTO.train_date"		:	config.station["train_date"],
			"leftTicketDTO.from_station"	:	utils.get(config.station["from_station_name"]),
			"leftTicketDTO.to_station"		:	utils.get(config.station["to_station_name"]),
			"purpose_codes"					:	"ADULT",
		}

		r = self.s.get(config.URL["monitor"], params=params)	
		try:
			if r.json()["status"] != True:
				ret["result_code"] = -2
				ret["result_message"] = r.json()["messages"] or "查票状态失败"
				Logger.info(ret["result_message"])
				return ret

			result = r.json()["data"]["result"]
			for i in result:
				l = i.split('|')
				if l[3] in config.monitor["car_num"]:
					for seat in config.monitor["seat"]:
						if l[seat] == "有" or l[seat].isdigit():
							Logger.info("检测到 %s %s %s" % (l[3], config.seat[seat], l[seat]))
							ret["result_code"] = 0
							ret["result_message"] = "%s %s %s" % (l[3], config.seat[seat], l[seat])
							ret["secret_str"] = l[0]
							ret["seatType"] = config.seat[seat]
							ret["car_num"] = l[3]
							return ret			
						else:
							Logger.info("检测到 %s %s %s" % (l[3], config.seat[seat], l[seat]))
				
			ret["result_code"] = -3
			ret["result_message"] = "没有检测到所需票"
			Logger.info("没有检测到所需票")
			return ret											
		except:
			ret["result_code"] = -1
			ret["result_message"] = "查询失败,请重试!"
			Logger.info("查询失败,请重试!")
			return ret
			
	def get_order(self, secret_str, seatType):
		ret = {
			"result_code"		: 0,
			"result_message"	: "",
		}
		#print (secret_str)
		secret_str = urllib.parse.unquote(secret_str) #urldecode

		r0 = self.s.post(config.URL["check_user"], data={"_json_att":""})
		try:
			if r0.json()["status"] != True or r0.json()["data"]["flag"] != True:
				ret["result_code"] = -1
				ret["result_message"] = "登录过期, 请重新登录"
				Logger.info("登录过期, 请重新登录")
				return ret
		except:
			ret["result_code"] = -1
			ret["result_message"] = "检测登录状态失败"
			Logger.info("检测登录状态失败")
			return ret

		params1 = {
			"secretStr"					: secret_str,
			"train_date"				: config.station["train_date"],
			"back_train_date"			: time.strftime('%Y-%m-%d',time.localtime(time.time())),
			"tour_flag"					: "dc",
			"purpose_codes"				: "ADULT",
			"query_from_station_name"	: config.station["from_station_name"],
			"query_to_station_name"		: config.station["to_station_name"],
			"undefined"					: "",
		}

		r1 = self.s.post(config.URL["submit_order_request"], data=params1)
		try:
			count = 1
			while r1.json()["status"] != True:
				time.sleep(3)
				count += 1
				if count > self.max_retry_times:
					ret["result_code"] = -2
					ret["result_message"] = "提交订单错误, 请重新登录"
					Logger.info(ret["result_message"])
					return ret
				Logger.info("提交订单错误, 正在重试 " + str(count))
				r1 = self.s.post(config.URL["submit_order_request"], data=params1)
				
		except:
			ret["result_code"] = -2
			ret["result_message"] = "提交订单错误, 请重新登录"
			Logger.info(ret["result_message"])
			return ret

		r2 = self.s.post(config.URL["initDc"], data={"_json_att":""})
		try:
			regx = re.search(r"var globalRepeatSubmitToken = '(.*?)';[\s\S]*?ticketInfoForPassengerForm=(.*?);", r2.text)
			submit_token = regx.group(1)
			ticketInfoForPassengerForm = json.loads(regx.group(2).replace("'", "\""))
			Logger.info("submit_token = %s" % submit_token)
		except:
			ret["result_code"] = -3
			ret["result_message"] = "initDc错误, 请重新登录"
			Logger.info(ret["result_message"])
			return ret

		r3 = self.s.post(config.URL["get_passengerDTOs"], data={"_json_att":"", "REPEAT_SUBMIT_TOKEN":submit_token})
		try:
			count = 1
			while r3.json()["status"] != True:
				time.sleep(3)
				count += 1
				if count > self.max_retry_times:
					ret["result_code"] = -7
					ret["result_message"] = "获取乘客信息失败"
					Logger.info(ret["result_message"])
					return ret
				Logger.info("get_passengerDTOs错误, 正在重试 " + str(count))
				r3 = self.s.post(config.URL["get_passengerDTOs"], data={"_json_att":"", "REPEAT_SUBMIT_TOKEN":submit_token})

			normal_passengers = r3.json()["data"]["normal_passengers"]
			for user in normal_passengers:
				if user["passenger_name"] == config.monitor["name"]:
					user_info = user
		except:
			ret["result_code"] = -7
			ret["result_message"] = "获取乘客信息失败"
			Logger.info(ret["result_message"])
			return ret


		passengerTicketStr = "%s,0,%s,%s,%s,%s,%s,N" % (seatType, user_info["passenger_type"], user_info["passenger_name"], user_info["passenger_id_type_code"], user_info["passenger_id_no"], user_info["mobile_no"])
		oldPassengerStr = "%s,%s,%s,%s_" % (user_info["passenger_name"], user_info["passenger_id_type_code"], user_info["passenger_id_no"], user_info["passenger_type"])
		params4 = {
			"cancel_flag"			: "2",
			"bed_level_order_num"	: "000000000000000000000000000000",
			"passengerTicketStr"	: passengerTicketStr,
			"oldPassengerStr"		: oldPassengerStr,
			"tour_flag"				: ticketInfoForPassengerForm["tour_flag"],
			"randCode"				: "",
			"whatsSelect"			: seatType,
			"_json_att"				: "",
			"REPEAT_SUBMIT_TOKEN"	: submit_token,

		}
		r4 = self.s.post(config.URL["check_order_info"], data=params4)
		try:
			count = 1
			while r4.json()["data"]["submitStatus"] != True:
				time.sleep(3)
				count += 1
				if count > self.max_retry_times:
					ret["result_code"] = -3
					ret["result_message"] = "确认订单信息错误, 请重新下单"
					Logger.info(ret["result_message"])
					return ret
				Logger.info("check_order_info错误, 正在重试 " + str(count))
				r4 = self.s.post(config.URL["check_order_info"], data=params4)
		except:
			ret["result_code"] = -3
			ret["result_message"] = "确认订单信息错误, 请重新下单"
			Logger.info(ret["result_message"])
			return ret

		params5 = {
			"train_date"			: utils.trans_date(config.station["train_date"]),
			"train_no"				: ticketInfoForPassengerForm["orderRequestDTO"]["train_no"],
			"stationTrainCode"		: ticketInfoForPassengerForm["orderRequestDTO"]["station_train_code"],
			"seatType"				: seatType,
			"fromStationTelecode"	: ticketInfoForPassengerForm["orderRequestDTO"]["from_station_telecode"],
			"toStationTelecode"		: ticketInfoForPassengerForm["orderRequestDTO"]["to_station_telecode"],
			"leftTicket"			: ticketInfoForPassengerForm["leftTicketStr"],
			"purpose_codes"			: ticketInfoForPassengerForm["purpose_codes"], #00代表学生，ADULT代表成人
			"train_location"		: ticketInfoForPassengerForm["train_location"],
			"_json_att"				: "",
			"REPEAT_SUBMIT_TOKEN"	: submit_token,
		}

		r5 = self.s.post(config.URL["get_queue_count"], data=params5)
		try:
			count = 1
			while r5.json()["status"] != True:
				time.sleep(3)
				count += 1
				if count > self.max_retry_times:
					ret["result_code"] = -4
					ret["result_message"] = "获取订单队列错误, 请重新下单"
					Logger.info(ret["result_message"])
					return ret
				Logger.info("get_queue_count错误, 正在重试 " + str(count))
				r5 = self.s.post(config.URL["get_queue_count"], data=params5)
		except:
			ret["result_code"] = -4
			ret["result_message"] = "获取订单队列错误, 请重新下单"
			Logger.info(ret["result_message"])
			return ret

		params6 = {
			"passengerTicketStr"		: params4["passengerTicketStr"],
			"oldPassengerStr"			: params4["oldPassengerStr"],
			"randCode"					: "",
			"purpose_codes"				: ticketInfoForPassengerForm["purpose_codes"], #00代表学生，ADULT代表成人
			"key_check_isChange"		: ticketInfoForPassengerForm["key_check_isChange"],
			"leftTicketStr"				: ticketInfoForPassengerForm["leftTicketStr"],
			"train_location"			: ticketInfoForPassengerForm["train_location"],
			"choose_seats"				: "",
			"seatDetailType"			: "000",
			"whatsSelect"				: seatType,
			"roomType"					: "00",
			"dwAll"						: "N",
			"_json_att"					: "",
			"REPEAT_SUBMIT_TOKEN"		: submit_token,
		}	

		r6 = self.s.post(config.URL["confirm_queue"], data=params6)
		try:
			count = 1
			while r6.json()["data"]["submitStatus"] != True:
				time.sleep(3)
				count += 1
				if count > self.max_retry_times:
					ret["result_code"] = -5
					ret["result_message"] = "确认订单错误, 请重新下单"
					Logger.info(ret["result_message"])
					return ret
				Logger.info("confirm_queue错误, 正在重试 " + str(count))
				r6 = self.s.post(config.URL["confirm_queue"], data=params6)
		except:
			ret["result_code"] = -5
			ret["result_message"] = "确认订单错误, 请重新下单"
			Logger.info(ret["result_message"])
			return ret

		for i in range(5):
			r7 = self.s.get(config.URL["query_order_wait_time"], params={"random":round(time.time()*1000), "tourFlag":ticketInfoForPassengerForm["tour_flag"], "_json_att":"", "REPEAT_SUBMIT_TOKEN":submit_token})
			try:
				if r7.json()["data"]["orderId"] != None:
					break
			except:
				pass
			time.sleep(4)
		try:
			if r7.json()["data"]["orderId"] == None:
				ret["result_code"] = -6
				ret["result_message"] = "订单已在排队, 但排队人数过多，建议重新下单"
				Logger.info(ret["result_message"])
				return ret
		except:
			ret["result_code"] = -6
			ret["result_message"] = "订单排队错误, 请重新下单"
			Logger.info(ret["result_message"])
			return ret

		r8 = self.s.post(config.URL["result_order"], data={"orderSequence_no":r7.json()["data"]["orderId"], "_json_att":"", "REPEAT_SUBMIT_TOKEN":submit_token})
		try:
			count = 1	
			while r8.json()["data"]["submitStatus"] != True:
				time.sleep(3)
				count += 1
				if count > self.max_retry_times:
					ret["result_code"] = -7
					ret["result_message"] = "下单失败"
					Logger.info(ret["result_message"])
					return ret
				Logger.info("result_order错误, 正在重试 " + str(count))
				r8 = self.s.post(config.URL["result_order"], data={"orderSequence_no":r7.json()["data"]["orderId"], "_json_att":"", "REPEAT_SUBMIT_TOKEN":submit_token})

			ret["result_code"] = 0
			ret["result_message"] = "下单成功"
			ret["station_train_code"] = ticketInfoForPassengerForm["orderRequestDTO"]["station_train_code"]
			return ret
		except:
			ret["result_code"] = -7
			ret["result_message"] = "下单失败"
			Logger.info(ret["result_message"])
			return ret

	def get_no_complete(self):
		ret = {
			"result_code"		: 0,
			"result_message"	: "",
		}

		for i in range(10):
			r = self.s.post(config.URL["queryMyOrderNoComplete"], data={"_json_att":""})
			if r.json()["status"] == True:
				ret["result_order"] = 0
				ret["result_message"] = "查询成功"
				ret["data"] = r.json()["data"]["orderDBList"][0]["tickets"][0]
				return ret

		ret["result_order"] = -1
		ret["result_message"] = "查询失败"
		return ret

	def logout(self):
		#退出登陆
		r = self.s.get(config.URL["login_out"])
		
		r1 = self.s.post(config.URL["uamtk"], data={"appid":"otn"})
		Logger.info(r1.text)


if __name__ == '__main__':
	is_login = False
	is_monitor = False
	is_get_order = False
	count = 1 #重试次数

	ticket = pass12306()

	while True:
		while is_login == False:
			ret_login = ticket.login()
			if ret_login["result_code"] == 0: # login successfully
				Logger.info("登录成功 %s" % ret_login["username"])
				is_login = True
				break
			else:
				Logger.info("登录失败 %s" % ret_login["result_message"])

		while is_monitor == False:
			ret_query = ticket.monitor()
			if ret_query["result_code"] == 0: #检测到票，跳出循环, 下单
				is_monitor = True
				Logger.info("检测到票 %s" % ret_query["result_message"])
				break
			else:
				time.sleep(1) #没有查询到票，sleep1秒后继续查询
				Logger.info("检测失败 %s 已查询次数 %d 次" % (ret_query["result_message"], count))
				count += 1
				

		while is_get_order == False:
			ret_order = ticket.get_order(ret_query["secret_str"], config.seatType[ret_query["seatType"]])
			if ret_order["result_code"] == 0: #下单成功
				is_get_order = True
				break
			else:
				time.sleep(2) #下单失败，sleep2秒后继续查询
				is_monitor = False
				break
		if is_get_order: break
	
	
	#发邮件通知用户支付
	ret_search_order = ticket.get_no_complete()
	if ret_search_order["result_code"] == 0:
		content = "%s 同志你好, 你选择从 【%s】 到 【%s】 的 %s 【%s车厢 %s %s】 【%s发车】 已经自动下单, 请在【20分钟内】去12306->【未完成订单中支付】! %s" % (config.monitor["name"], 
			ret_search_order["data"]["stationTrainDTO"]["from_station_name"], 
			ret_search_order["data"]["stationTrainDTO"]["to_station_name"], 
			ret_search_order["data"]["stationTrainDTO"]["station_train_code"], 
			ret_search_order["data"]["coach_no"], 
			ret_search_order["data"]["seat_name"], 
			ret_search_order["data"]["seat_type_name"], 
			ret_search_order["data"]["start_train_date_page"], 
			config.URL["initNoComplete"])
	else:
		content = "%s 同志你好, 你选择从 【%s】 到 【%s】 的 %s 【%s】 【%s发车】 已经自动下单, 请在【20分钟内】去12306->【未完成订单中支付】! %s" % (
			config.monitor["name"],
			config.station["from_station_name"],
			config.station["to_station_name"],
			ret_query["car_num"],
			ret_query["seatType"],
			config.station["train_date"],
			config.URL["initNoComplete"])
	Logger.info(content)
	send_email.send(content)

	