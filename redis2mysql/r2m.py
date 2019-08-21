import redis
import json
import pymysql
import re


class Shift():
    def __init__(self):
        redis_args = {
            "host":"localhost",
            "port":6379,
            "db":0,
            }
        mysql_args = {
            "host":"localhost",
            "user":"root",
            "password":"abc",
            "port":3306,
            "db":"mydb2",
        }
        self.r = redis.StrictRedis(**redis_args)
        # self.q = pymysql.connect(host="localhost",user="root",password="abc", port=3306, db="mydb2")
        self.q = pymysql.connect(**mysql_args)
        self.cursor = self.q.cursor()

    def R2M(self):
        json_list = self.r.lrange('stone_salve:items',0,0) # list type
        for vo in json_list:
            data = json.loads(vo) # loads成python (因為先前在dump之前是dict，所以loads回來也是dict格式)
            keys = ','.join(data.keys()) # str type ===> key1, key2, key3, ...
            values = ','.join(['%s']*len(data)) # str type ===> value1, value2, value,...
            sql = 'insert into kingstone_books(%s) values(%s)'%(keys,values)
            data['img'] = str(data['img'])
            
            print(data.values())
            
            
            self.cursor.execute(sql,tuple(data.values())) # 批量執行的方法 
            self.q.commit()
        self.cursor.close()
        self.q.close()
       

def main():
    Shift().R2M() 


if __name__ == '__main__':
    main()

    

