import json
import csv

from FilePaths import ACCOUNTS_FILE,STATS_FILE,SITES_FILE,ITEMS_FILE, \
    PROXY_FILE, TASKS_FILE, LOGS_FILE



#Tasks
#Returns task.json
def getTasksData():

    with open(TASKS_FILE, 'r') as data:
        json_data = json.load(data)

    return json_data

#Adds data to the end of tasks.json
def addTasksData(data):
    """
    :param data:
    :return:
    """

    with open(TASKS_FILE,'r') as task_data:
        json_data = json.load(task_data)

    task_data.close()

    json_data[len(json_data)] = data

    with open(TASKS_FILE,'w') as outfile:
        json.dump(json_data, outfile,indent=4)

    outfile.close()

#Sets Task data to the data
#used in delete tasks
def setTasksData(data):

    with open(TASKS_FILE,'w') as outfile:
        json.dump(data, outfile,indent=4)

    outfile.close()

#Accounts
#Get account data from files/account.json
def getAccountsData():
    """
    :return: the json data from files/auto_fill.json
    """
    with open(ACCOUNTS_FILE, 'r') as data:
        json_data = json.load(data)

        return json_data

#Add account to files/account.json
def addAccount(account_name,data):
    with open(ACCOUNTS_FILE,'r') as account_data:
        json_data = json.load(account_data)

    account_data.close()
    json_data[account_name] = data

    with open(ACCOUNTS_FILE,'w') as outfile:
        json.dump(json_data,outfile,indent=4)

    outfile.close()

#Delete account from files/account.json
def deleteAccount(account_name):
    with open(ACCOUNTS_FILE,'r') as account_data:
        json_data = json.load(account_data)

    if account_name in json_data:
        del json_data[account_name]

    with open(ACCOUNTS_FILE,'w') as outfile:
        json.dump(json_data,outfile,indent=4)

    account_data.close()

#Log
def getLogData(rows):
    with open(LOGS_FILE, 'r') as log_file:
        log_data = csv.reader(log_file)

        log_header = next(log_data)

        data = []
        i = 0
        for row in reversed(list(log_data)):
            if i >= rows:
                break
            if len(row) != 0:
                data.append(row)
                i += 1

        return log_header,data

def addLog(data):
    with open(LOGS_FILE, 'a', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(data)



#Proxy
def getProxyData():
    with open(PROXY_FILE, 'r') as data:
        json_data = json.load(data)

        return json_data

def addProxy(name,ip):
    with open(PROXY_FILE, 'r') as data:
        json_data = json.load(data)

    data.close()
    if name not in json_data:
        json_data[name] = {
            "IP" : ip
        }


    with open(PROXY_FILE,'w') as outfile:
        json.dump(json_data,outfile,indent=4)

    outfile.close()

def deleteProxy(name):
    with open(PROXY_FILE, 'r') as data:
        json_data = json.load(data)

    data.close()

    if name in json_data:
        del json_data[name]

    with open(PROXY_FILE, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

    outfile.close()
