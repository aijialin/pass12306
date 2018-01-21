# pass12306

一个模拟12306查询余票并且自动下单的脚本，你只需要填写乘车日期，区间以及乘车人即可，你也可以填上用于抢票成功后接受  
不支持识别验证码，需要手动输入。  

## 填写配置信息
打开config.py文件找到如下配置项  
![image][https://github.com/aijialin/pass12306/blob/master/image/config.png]

## 运行程序

### 手动输入验证码
当运行程序时，会要求手动输入验证码，如下  
![image][https://github.com/aijialin/pass12306/blob/master/image/yanzhengma.jpg]

### 验证码的输入形式
12306是采用图片验证码，通过鼠标点击的位置转换为坐标进行识别，参考下图  
![image][https://github.com/aijialin/pass12306/blob/master/image/verification.png]  
你只需要输入对应位置的图片编号即可  
![image][https://github.com/aijialin/pass12306/blob/master/image/log.png]

如果成功检测到余票，程序会自动下单并且通过你配置的邮箱给你发送一封邮件。  
![iamge][https://github.com/aijialin/pass12306/blob/master/image/email.png]

## 运行日志
程序运行后会在运行目录产生日志，当然你也可以使用log模块下的set_logging方法关闭它们。

## 关于
仅用来学习交流，严禁用于非法用途。

