import sys
import os
import time

class DATA:

    filecount = 0

    def __init__(self,path):
        self.PATH = path
        if not os.path.exists(path):
            os.makedirs(path)
        now_time = time.localtime()
        self.timestart = ("%02d_%02d_%02d_%02d_%02d_%02d" %(now_time[3],now_time[4],now_time[5],now_time[2],now_time[1],now_time[0]))
        result_file = open(self.PATH + "\\Results_%s.txt" %(self.timestart), "w")
        result_file.close()

    def WRITE(self,input):
        result_file = open(self.PATH + "\\Results_%s.txt" %(self.timestart), "a")
        result_file.write(input)
        result_file.close()


