import pandas as pd
import sys
import os.path
import datetime

import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

class File(object):

    def __init__(self, work_path, file_name, encoding="UTF-8"):
        self.work_path = self.__set_work_path(work_path)
        self.file_name = file_name
        self.encoding = encoding

    def __set_work_path(self, work_path):
        if os.path.dirname(sys.argv[0]) == "":
            work_path = work_path
        else:
            work_path = os.path.dirname(sys.argv[0])
        return work_path


class Example(File):

    def __init__(self, work_path, file_name, encoding="UTF-8"):
        super().__init__(work_path, file_name, encoding="UTF-8")
        self.df = pd.read_csv(os.path.join(work_path, file_name),
                              encoding=self.encoding,
                              engine='python',
                              header=None)

    def clean_df(self):
        temp_df = self.df[0].str.split("\t", expand=True)
        temp_df[0] = pd.to_datetime(temp_df[0])

        temp_df = temp_df.set_index(0)

        start=[]
        end=[]
        for my_iter, value in enumerate(temp_df.index[:-1]):
            time_delta=(int(
                ((temp_df.index[my_iter + 1] - value).total_seconds()) / 180))
            if time_delta > 2:
                start.append (temp_df.index[my_iter])
                end.append(temp_df.index[my_iter+1])
        length=len(temp_df)
        first_time=temp_df.index[0]
        last_time=temp_df.index[length-1]
        self.df=temp_df
        return pd.Series(start),pd.Series(end),first_time,last_time



    def find_value(self,start,end,first_time,last_time):

        temp_df = self.df
        timedel=datetime.timedelta(days=7,hours=0,minutes=0,seconds=0)

        start_last_week=start-timedel
        end_last_week=end-timedel

        start_next_week=start+timedel
        end_next_week=end+timedel

        if end_last_week < first_time:
            df = temp_df[start_next_week:end_next_week]
            new_df = pd.DataFrame(data=df.values, index=df.index - timedel, columns=df.columns)

        else:
            df= temp_df[start_last_week:end_last_week]
            new_df = pd.DataFrame(data=df.values, index=df.index + timedel, columns=df.columns)

        self.df=pd.concat([temp_df,new_df])
        #print(type(self.df))
        #print(self.df)



    def add_value(self,start,end,first_time,last_time):
        for i in range(len(start)):
            v=self.find_value(start[i],end[i],first_time,last_time)

if __name__ == "__main__":
    work_path = '/Users/yang/PycharmProjects/FirstProjet/Test/third_month'
    file_name = "Ident_15.csv"
    encoding = "UTF-8"
    plotly.tools.set_credentials_file(username='xinyue', api_key='TN49uoyAn5VXfN6bpAAw')

    csv = Example(work_path, file_name, encoding)

    start,end,first_time,last_time=csv.clean_df()


    #csv.add_value(start,end,first_time,last_time)

    #csv.df.sort_index(inplace=True)
    #csv.df.to_csv('Ident_15_new.csv', sep='\t', encoding='utf-8')

    #d = [go.Scatter(
    #    x=csv.df.index,
    #    y=csv.df.values)]
    #layout = dict(title="Prétraitement")
    #fig = dict(data=d, layout=layout)
    #py.plot(fig, filename="Debit d'avril")

