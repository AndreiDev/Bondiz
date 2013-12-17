from datetime import datetime

def taskDebug(message):
    f = open('taskLog.txt','a')
    f.write(str(datetime.now()) + ' | ' + message + '\n')
    f.close()
    #print(str(datetime.now()) + ' | ' + message)