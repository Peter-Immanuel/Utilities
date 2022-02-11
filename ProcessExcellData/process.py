from datetime import date as dt
import openpyxl
import pandas as pd



# Functions to generate the entire DataFrame of Data including calculated result for DCR, TCH_Cong and CSSR
def computeValues():
        database = {}
        sheet_month_index = []

        # sheet_list = ["T-Mobile","MTN NG", "etisalat","Glo NG", "Airtel NG", "9mobile"]
        sheet_list = ["T-Mobile","MTN NG",]

        for sheet_name in sheet_list:        
                # setup
                df = pd.read_excel("data.xlsx", sheet_name=sheet_name, engine='openpyxl')
                month_index = []
                month_database = []
                date = df["createdAt"]

                # get the value of the sections within dataframe
                for i in range(len(date)):
                        if type(date[i])==float:
                                month_index.append(i)
                month_index.append(len(date))

                # append the sheet indexies into sheet_month_index
                sheet_month_index.append(month_index)

                # looping through the sections within the dataframe
                for i in range(len(month_index)-1):

                        value = month_index[i+1]-month_index[i]-1       #Calculate the amount of each month's data

                        test_df = df
                        current_df = test_df.iloc[month_index[i]:month_index[i+1]]   # split dataframe to obtain dataset for  current month

                        # calculation of DCR 
                        num_of_true = list(current_df["callDropped"]).count(1)
                        DCR = round(((num_of_true/value) * 100), 4)

                        # calculation of TCH-Cong
                        congestion_true = list(current_df["congested"]).count(1)
                        TCH_cong = round(((congestion_true/value) * 100), 4)

                        # calculation of CSSR
                        setup_true = list(current_df["setUpSuccessful"]).count(2)
                        CSSR = round(((setup_true/value) *100),4)

                        date_stamp = list(current_df["createdAt"])[1]

                        print(date_stamp)
                        # populate the database
                        # key = "month "+ str(i)
                        month_database.append((DCR, TCH_cong, CSSR))
                database[sheet_name]= month_database
                print(month_database)
        return (sheet_month_index, database)
               
def updateValues(filename, save_as, month_index_list, sheet_database):
        df_writer_list = []        # list to keep track of the sheet name and data frame
        sheet_database_key =  list(sheet_database.keys())       #get a list of the sheet names

        for i in range(len(sheet_database_key)):        # using a loop of length equal to the number of sheets obtained
                key = sheet_database_key[i]                  # get the ith key in the list
                value = sheet_database[key]                 # get the corresponding value of the ith key from the sheet database

                df = pd.read_excel(filename, sheet_name=key, engine="openpyxl")         #load the dataframe from sheet name
                month_index = month_index_list[i]       # get the ith item in the month_index list

                for i in range(len(month_index)-1):
                        index = month_index[i] + 1              # obtain the start of each month
                        df.at[index,"DCR"] = value[i][0]        #  update the value of DCR
                        df.at[index, "TCH-Cong"] = value[i][1]  # update the value of TCH-Cong
                        df.at[index, "CSSR"] = value[i][2]              # update the value of the CSSR
                df_writer_list.append((key,df))


        # create a new excel file and update the dataframe 
        with pd.ExcelWriter(save_as) as writer:
                for i in range(len(df_writer_list)):
                        df_tuple = df_writer_list[i]
                        sheet_name, df = df_tuple
                        df.to_excel(writer, sheet_name=sheet_name)
                        




# Functions to generate a Summary of the calculated Results for DCR, TCH_Cong and CSSR

name_of_months ={
        "01" :"January", "02" :"February", "03" :"March", "04" :"April",
        "05" :"May", "06" :"June", "07" :"July", "08" :"August",
        "09" :"September", "10" :"October", "11" :"November", "12" :"December"
}

def formatDate(date):
        if type(date) is not str:
                return False
        datetimeStamp = date
        date, time = datetimeStamp.split(" ")
        date = date[:7]
        year, month = date.split("-")
        month = name_of_months[month]
        return (month+ " "+year)



def resultComputeValues(filename):
        database = {}
        sheet_month_index = []

        sheet_list = ["T-Mobile","MTN NG", "etisalat","Glo NG", "Airtel NG", "9mobile"]
        # sheet_list = ["T-Mobile","MTN NG",]

        for sheet_name in sheet_list:  
                print("\n")
                print("Calculating Values for sheet " + sheet_name)      
                # setup
                filename = str(filename)
                df = pd.read_excel(filename, sheet_name=sheet_name, engine='openpyxl')
                month_index = []
                month_database = []
                date = df["createdAt"]

                # get the value of the sections within dataframe
                for i in range(len(date)):
                        print(f"calculating month index {i}") 
                        if type(date[i])==float:
                                month_index.append(i)
                month_index.append(len(date))

                # append the sheet indexies into sheet_month_index
                sheet_month_index.append(month_index)

                # looping through the sections within the dataframe
                for i in range(len(month_index)-1):

                        value = month_index[i+1]-month_index[i]-1       #Calculate the amount of each month's data
                        print(f"Value is {value}")

                        test_df = df
                        current_df = test_df.iloc[month_index[i]:month_index[i+1]]   # split dataframe to obtain dataset for  current month
                        
                        # calculation of DCR 
                        num_of_true = list(current_df["callDropped"]).count(1)
                        DCR = round(((num_of_true/value) * 100), 4)

                        # calculation of TCH-Cong
                        congestion_true = list(current_df["congested"]).count(1)
                        TCH_cong = round(((congestion_true/value) * 100), 4)

                        # calculation of CSSR
                        setup_true = list(current_df["setUpSuccessful"]).count(2)
                        CSSR = round(((setup_true/value) *100),4)

                        date_stamp = list(current_df["createdAt"])[1]

                        string_date = formatDate(date_stamp)
                        month_database.append((string_date, DCR, TCH_cong, CSSR))
                database[sheet_name]= month_database
                print(f"Values for {sheet_name} completely calculated" )
        
        print("Values Completely calculated")
        print("\n")
        return (database)

def resultValues(save_as, sheet_database):
        sheet_names = list(sheet_database.keys())
        df_writer_list   = []      #List to hold values for each sheet and its dataframe

        unit_percent = round((100/len(sheet_names)),2)
        total_percent = 0
        for sheet in sheet_names:
                total_percent += unit_percent
                print(f"Preparing Result------  {round(total_percent,2)} %")
                sheet_value = sheet_database[sheet]  # extract the tuple (month, DCR,TCH_Cong)
                index  = [] # list to hold month details
                cal_value = []  # list to hold DCR,TCH_Cong, CSSR per month
                for data in sheet_value:
                        month = data[0]
                        index.append(month)
                        value = data[1:] 
                        cal_value.append(value)
                
                df = pd.DataFrame(
                        cal_value,
                        index = index,
                        columns = ["DCR", "TCH_Cong", "CSSR"]
                )

                df_writer_list.append((sheet, df))

        print("\n")
        print("Result Completed, Creating Excel Document for Result... ")
        # create a new excel file and update the dataframe 
        with pd.ExcelWriter(save_as) as writer:
                for i in range(len(df_writer_list)):
                        df_tuple = df_writer_list[i]
                        sheet_name, df = df_tuple
                        df.to_excel(writer, sheet_name=sheet_name)

        print(f"Your Document is Ready as {save_as}")
                        



if __name__ =="__main__":

        # This part of the script is used to generate the full result        
        filename = "Processing_Nov_20.xlsx"
        # filename = "data.xlsx"
        save_as = "resultSummary1.xlsx"
        #month_index, sheet_database = resultComputeValues()
        #updateValues(filename=filename, save_as=save_as, monpythth_index_list=month_index,sheet_database=sheet_database)



        # This part of the script is used to generate a Summary of the result
        database =  resultComputeValues(filename=filename)
        resultValues(save_as, sheet_database=database)


        
        

