import datetime as dt
import random as rd
import requests as rq
import json
import time

'''
tank size = 4000Litre
Size = 1850mm = 1.85m
sensor distance to full tank = 0.15m 

Fields:
        -water_consumed - Field 1
        -pump_status - field 2
        -battery_condition - field3
        -water-level - field 4

Algorithm:
        - generate random values for  water consumed between: 
        - calculate water level
        - create header
        - create request


        "created_at": "DATETIME_STAMP",
                                "field1": FIELD1_VALUE,
                                "field2": FIELD2_VALUE,
                                "field3": FIELD3_VALUE,
                                "field4": FIELD4_VALUE,
                                "field5": FIELD5_VALUE,
                                "field6": FIELD6_VALUE,
                                "field7": FIELD7_VALUE,
                                "field8": FIELD8_VALUE,
                                "Latitude": LATITUDE_VALUE,
                                "Longitude": LONGITUDE_VALUE,
                                "Elevation": ELEVATION_VALUE,
                                "Status": "STATUS_STRING"
                        },
'''



def generate_timestamps():

        # function to generate time for an hour in ISO 1801 
        init_date = dt.datetime.now() - dt.timedelta(days=7)
        time_stamp_list = []
        for i in range(60):
                new_time = init_date + dt.timedelta(minutes=i+1, seconds=i+30)
                new_time = str(new_time.isoformat())
                new_time =  new_time.replace("T", " ")
                house = new_time.split('.')
                
                my_time = house[0] + " +0100"

                time_stamp_list.append(my_time)
        return time_stamp_list


def generate_values():

        # function to generate random values for (water consumed, pump_status, battery_condition, water level)
        dp1 = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        dp2 = [0.00,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009]
        device_value = list()

        water_level = 0
        for i in range(60):
 
                # water consumed, pump_status, battery_condition, water level
                # correct the water value to continuouslu increase during the first upload set
                if i == 0:
                        water_level += rd.choice(dp2)
                else:
                        water_level +=  0.02 + rd.choice(dp2)
                device_value.append( ( (rd.randint(0,10) + rd.choice(dp1)),1,1, round(water_level,2)) )
        return device_value


def update_thingspeak(time_stamp_list, value_list):
        endpoint = "https://api.thingspeak.com/channels/1592145/bulk_update.json"
        # endpoint_single  = "https://api.thingspeak.com/update.json"
        header={
                "Accept": "*/*",
                "User-Agent": "Thunder Client (https://www.thunderclient.io)",
                "Content-Type": "application/json"     
        }
        payload = {
                "write_api_key": "39MRAV5ZZPDNDTC5",
                "updates": []
        }
        
        key_list = ["created_at", "field1", "field2", "field3", "field4", "Status"]
                
        
        for i in range(len(time_stamp_list)):
                instance = dict()
                for j in range(len(key_list)-1):
                        instance[key_list[j]]= time_stamp_list[i]
                        values = value_list[i]
                        for k in range(4):
                                instance[key_list[k+1]]=values[k]
                instance['status']= 'good'


                payload['updates'].append(instance)

        json_payload = json.dumps(payload, indent=4)
        data= (json_payload)
        update = rq.post(url=endpoint, data=json_payload, headers=header)
        print(update.status_code)
        print(update.json())


if __name__ =="__main__":
        timestamp=generate_timestamps()
        value_list = generate_values()
        update_thingspeak(timestamp,value_list)

        