from datetime import date as dt
import openpyxl
import pandas as pd


# function to calculate call Dropped
def computeValues():
        # setup
        month_index = [0]
        database = {}
        df = pd.read_excel("data.xlsx", sheet_name="MTN NG", engine='openpyxl')
        date = df["createdAt"]

        # get the value of the intersection within dataframe
        for i in range(len(date)):
                if type(date[i])==float:
                        month_index.append(i)
        month_index.append(len(date))


        # looping through the intersection index within the dataframe
        for i in range(len(month_index)-1):
                value = month_index[i+1]-month_index[i]-1

                # Calculate the values of the DCR, TCH-Cong and CSSR
                current_df = df.iloc[month_index[i]:month_index[i+1]]

                # calculation of DCR 
                num_of_true = list(current_df["callDropped"]).count(1)
                DCR = round(((num_of_true/value) * 100), 4)

                # calculation of TCH-Cong
                congestion_true = list(current_df["congested"]).count(1)
                TCH_cong = round(((congestion_true/value) * 100), 4)

                # calculation of CSSR
                setup_true = list(current_df["setUpSuccessful"]).count(2)
                CSSR = round(((setup_true/value) *100),4)

                key = "month "+ str(i)
                database[key]=(i, (DCR, TCH_cong, CSSR))
        
        return (database)

#  [17, 186, 348, 610, 709, 767, 807, 889, 926, 1072, 1427, 1574, 1658, 1716, 2233]    

def updateSheet():
        df_1 = pd.read_excel("data.xlsx", sheet_name="MTN NG", engine="openpyxl")


        _df_1 = df_1.iloc[0:17]

        _df_1["TCH-Cong"][0]=15
        print(_df_1)






if __name__ =="__main__":
        # computeValues()
        updateSheet()