import os,time

seat = {
	"yidengzuo" : 31,
	"erdengzuo" : 30,
	"ruanwo"	: 23,
	"yingwo"	: 28,
	"yingzuo"	: 29,
	"wuzuo"		: 26,
	26			: "无座",
	29			: "硬座",
	28			: "硬卧",
	23			: "软卧",
	30			: "二等座",
	31 			: "一等座",
}
#############################################配置区域################################################
station  = {
	"train_date"			: "2018-02-02",			#乘车日期
	"from_station_name"  	: "北京",				#起点
	"to_station_name"		: "上海",				#终点
}
monitor = {
	"car_num"	: ("G101", "G103"),					#列车编号 例如("K998",) 可监控多个
	"seat"		: (seat["yidengzuo"], ),			#座位类别，例如硬座为(seat["yingzuo"],) 可监控多种
	"name"		: "张三丰",							#乘车人姓名，例如"张三丰"
}

username = "xxxxxxxxxx@qq.com"						#12306账号
password = "xxxxxxxxxx"								#12306密码
email	 = "xxxxxxxxxx@qq.com"						#订票成功后接受通知结果的邮箱

#发送通知信息的邮箱用户/密码  
mail_username = 'xxxxxxxxxx@qq.com'  
mail_password = 'xxxxxxxxxx' 						#此处有可能是填写授权码，具体查看邮箱设置
#####################################################################################################

timeout = (3.05, 27)

yzmpath = os.getcwd() + "/yanzhengma.jpg"

cookies = {
	"RAIL_EXPIRATION"	:	"1516122298323",
	"RAIL_DEVICEID"		:	"Yq18FNnmtkMoC8HhB3sx8Mg4DBahGvpnVNwuJHkyy0Hbwpfp9-A_gGKptztEmJG_gEBA-wRPUSBPOHI8bwm-H6vCBJvbdoV3e-g-bvjzZkpGIMTE1x2",
}

headers = {
	"Content-Type"			: "application/x-www-form-urlencoded; charset=utf-8",
	"USER-AGENT"			: "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36",
	"X-Requested-With"		: "xmlHttpRequest",
	"Referer"				: "https://kyfw.12306.cn/otn/login/init",
	"Accept"				: "*/*",
}

URL = {
	"login_out"				: "https://kyfw.12306.cn/otn/login/loginOut",
	"login"					: "https://kyfw.12306.cn/passport/web/login",
	"login_init"			: "https://kyfw.12306.cn/otn/login/init",
	"check_url"				: "https://kyfw.12306.cn/passport/web/auth/uamtk", #是否登陆
	"captcha"				: "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&" + str(time.time()),
	"captcha_check"			: "https://kyfw.12306.cn/passport/captcha/captcha-check",
	"err_url"				: "http://www.12306.cn/mormhweb/logFiles/error.html",
	"uamauthclient"			: "https://kyfw.12306.cn/otn/uamauthclient",
	"uamtk"					: "https://kyfw.12306.cn/passport/web/auth/uamtk",

	"monitor"				: "https://kyfw.12306.cn/otn/leftTicket/queryZ",

	"check_user"			: "https://kyfw.12306.cn/otn/login/checkUser",
	"submit_order_request"	: "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest",
	"initDc"				: "https://kyfw.12306.cn/otn/confirmPassenger/initDc",
	"get_passengerDTOs"		: "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs",
	"check_order_info"		: "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo",
	"get_queue_count"		: "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount",
	"confirm_queue"			: "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue",
	"query_order_wait_time"	: "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime",
	"result_order"			: "https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue",

	"initNoComplete"		: "https://kyfw.12306.cn/otn/queryOrder/initNoComplete",
	"queryMyOrderNoComplete": "https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete",
}
seatType = {
	"硬卧"	: '3',
	"软卧"	: '4',
	"二等座"	: 'O',
	"一等座"	: 'M',
	"硬座"	: '1',
	"无座"	: '1',
}
LOGFILEDIR = os.getcwd() + '/'