
import MySQLdb as mysql
import faker
import faker_cloud
import faker_extras
import requests
import json
import numpy as np

def insert(db):
    fake = faker.Factory.create(locale='zh_CN')
    print("fake uuid")
    for i in range(1,101):
        print(fake.uuid4())
    print("fake date")
    for i in range(1,21):
        print(fake.date_time_this_month())
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print ("Data Version:%s" % data)
    db.close()

def urlstr(pageNo,pageSize=200,syear="2018",smonth="12",sday="01",shour="00",smin="00",ssecond="00",\
           eyear="2019",emonth="01",eday="01",ehour="00",emin="00",esecond="00"):
    url = str('http://10.3.9.236:8899/vehiclePass/searchMotorVehicles?\
pageSize={0}&pageNo={1}&startTime={2}-{3}-{4}%20{5}%3A{6}%3A{7}&endTime={8}-{9}-{10}%20{11}%3A{12}%3A{13}')\
.format(pageSize,pageNo,syear,smonth,sday,shour,smin,ssecond,eyear,emonth,eday,ehour,emin,esecond) 
    return url

def fakeplate(num:int):
   fake = faker.Factory().create("zh_CN")
   plates = list()
   for i in range(num):
       s = str("川{0}").format(fake.license_plate())
       s = s.replace(" ","")
       s = s.replace("-","")
       plates.append(s)
   return tuple(plates)

if __name__ == '__main__':
   # db = mysql.connect("localhost","root","guo","db_ga_viid",charset='utf8')
   # insert(db)

   plates = fakeplate(1000)#制作随机1000条假车牌
   maxpageSize = 200#http请求最大pageSize
   print(urlstr(1))

   html = requests.get(urlstr(1))
   code = html.encoding
   print(code)
   c = html.json()
   total = c["data"]["data"]["total"]
   print(type(total))
   epoch = total//maxpageSize + 1
   #file = open(".\extradata.txt",mode='w',encoding=code)
   for i in range(1,epoch):
      c.clear()
      c = requests.get(urlstr(i)).json()
      list_json = c["data"]["data"]["list"]
      list_i = list()
      for j in range(200):
          plateNo = list_json[j]["plateInfo"]
          if plateNo == "车牌":
              plateNo = plates[np.random.randint(low=0,high=1000)]
          tuple_j = (plateNo,\
                          list_json[j]["id"],\
                          list_json[j]["longitude"],\
                          list_json[j]["latitude"],\
                          list_json[j]["vehicleColor"],\
                          list_json[j]["vehicleType"],\
                          list_json[j]["relatedCameraIndexCode"],\
                          list_json[j]["passTimeStr"])
          list_i.append(tuple_j)#一次要插入数据库的数据
      print(list_i)
          #print(list_json[j]["plateInfo"]) 
       #file.write(requests.get(urlstr(i)).text)
       #print(str("page {0} finished!!!").format(i))
   c.clear()
   c = requests.get(urlstr(epoch))
   for i in range(total%maxpageSize):
       print(i)
   
   print("finish")