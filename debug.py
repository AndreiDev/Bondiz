from datetime import datetime

def debug(message):
    f = open('log.txt','a')
    f.write(str(datetime.now()) + ' | ' + message + '\n')
    f.close()
    #print(str(datetime.now()) + ' | ' + message)