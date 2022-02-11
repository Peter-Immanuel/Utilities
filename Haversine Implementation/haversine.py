import math



class HaversineDistance:
        radius = 6371
        def __init__(self, origin:str, destination:str):
                self.latA, self.lonA = origin.split(" ")
                self.latB, self.lonB = destination.split(" ")        
                self.__obtainDistance()

        
        def __toRad(self):
                self.latA = float(self.latA[0:len(self.latA)-1]) * math.pi/180         # Strip string of Pole direction and convert to number
                self.lonA = float(self.lonA[0:len(self.lonA)-1])* math.pi/180       # Strip string of Pole direction and convert to number
                self.latB = float(self.latB[0:len(self.latB)-1])* math.pi/180           # Strip string of Pole direction and convert to number
                self.lonB = float(self.lonB[0:len(self.lonB)-1])* math.pi/180        # Strip string of Pole direction and convert to number

                # obtain difference in between origin and destination 
                lat_dif = self.latB -self.latA
                lon_dif = self.lonB -self.lonA
                return (lat_dif,lon_dif)
                
        def __obtainDistance(self):
                lat_dif, lon_dif = self.__toRad()
                distance_initial = pow(math.sin(lat_dif/2),2)  + (math.cos(self.latA)*math.cos(self.latB)* pow((math.sin(lon_dif/2)),2))
                self.final_disatnce = 2*self.radius*math.asin(math.sqrt(distance_initial))
                 

        def __repr__(self):
                return f"{round(self.final_disatnce,4)}"



print(HaversineDistance('51.5007N 0.1246W', "40.6892S 74.0445E"))
        