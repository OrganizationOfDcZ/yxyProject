# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 20:59:03 2018

@author: Administrator
"""
import sys
import os.path 
import xlrd
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly
import plotly.graph_objs as go

class File(object):
    
    def __init__(self,work_path,file_name,encoding="UTF-8"):
        self.work_path = self.__set_work_path(work_path)
        self.file_name = file_name
        self.encoding = encoding
        
    def __set_work_path(self,work_path):
        if os.path.dirname(sys.argv[0]) == "":
            work_path = work_path
        else:
            work_path = os.path.dirname(sys.argv[0])
        return work_path
    
class YxyExcel(File):
    
    def __init__(self,work_path,file_name,encoding="UTF-8"):
        super().__init__(work_path,file_name,encoding="UTF-8")
        self.excel = xlrd.open_workbook(os.path.join(work_path,file_name))

            
        
if __name__ == "__main__":
    work_path = r'/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/PublicTransport'
    file_name = "CTS_validations-2016_Fichier-OK-LT_Calendrier.xlsx"
    encoding = "utf-8"
    plotly.tools.set_credentials_file(username='xinyue', api_key='TN49uoyAn5VXfN6bpAAw')
    excel = YxyExcel(work_path,file_name,encoding)
    res_dict = {}
    for table in excel.excel.sheets():
        #table = excel.excel.sheets()[1]
        nrow_start = 4 - 1
        ncol_start = ord("G") - 64 - 1
        ncol_space = ord("M") - ord("G")
        if len(table.name) > len("Data") and table.ncols > (ncol_start + (12 - 1) * ncol_space):
            ts = pd.date_range(start="01/01/2017",periods=365)
            temp_series = pd.Series(index=ts)
            for time in ts:
                row = nrow_start+(time-pd.datetime(year=time.year,month=time.month,day=1)).days
                col = ncol_start+(time.month-1)*ncol_space
                temp_series[time] = table.cell(row,col).value
            res_dict[table.name] = temp_series
        else:
            res_dict[table.name] = None
    # exemple for visualizing the Tickets of bus line 63


    bus63=res_dict['Calendrier Bus']
    bus63.to_csv('bus2016.csv', sep='\t', encoding='utf-8')
    # print(number_of_tickets.index)
    # plt.plot(number_of_tickets.index,number_of_tickets.values)
    # plt.show()
    #
    # d = [go.Scatter(
    #    x=bus63.index,
    #    y=bus63.values)]
    # layout = dict(title="bus line 63 ")
    # fig = dict(data=d, layout=layout)
    # py.plot(fig, filename="exemple")

