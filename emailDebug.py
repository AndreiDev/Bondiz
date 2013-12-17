from datetime import datetime

def emailDebug(message):
    f = open('emailLog.txt','a')
    f.write(str(datetime.now()) + ' | ' + message + '\n')
    f.close()
    #print(str(datetime.now()) + ' | ' + message)