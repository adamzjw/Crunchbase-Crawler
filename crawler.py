#Data crawler via CrunchBase API
from datetime import datetime
import time
import urllib
import json

#I/O
def readFetchList():
    permalinks = []

    with open('./fetch_list.txt') as file:
        for line in file:
            permalinks.append(line.strip("\n"))

    return permalinks

def readAPIKeys():
    keys = []

    with open('./keys.txt') as file:
        for line in file:
            keys.append(line.strip())

    return keys

def readLog():
    log = []

    with open('./log.txt') as file:
        for line in file:
            log.append(int(line.strip("\n")))

    return log
	
def updateLog(log):
    with open('./log.txt', 'w') as file:
        for l in log:
            s = '%d\n' % l
            file.write(s)

def readStatus():
    lastUpdated = 0
    lastUpdatedDate = None
    dailyCount = {}

    with open('./status.txt') as file:
        lastUpdated = int(file.next().strip('\n'))
        lastUpdatedDate = datetime.strptime(file.next(), '%Y-%m-%d %H:%M:%S.%f\n')

        for line in file:
            key, count = line.strip('\n').split(" ")
            dailyCount[key] = int(count)

    return lastUpdated, lastUpdatedDate, dailyCount

def updateStatus(lastUpdated, lastUpdatedDate, dailyCount):
    with open('./status.txt', 'w') as file:
        file.write('%d\n' % lastUpdated)
        file.write(str('%s\n' % lastUpdatedDate))

        for key in dailyCount:
            s = '%s %d\n' % (key, dailyCount[key])
            file.write(s)

def fetchOneCompany(permalink, key):
    filename = permalink.split('/')
    filename = filename[len(filename)-1]

    api_path = 'https://api.crunchbase.com/v/2%s?user_key=%s' % (permalink, key)

    try:
        response = urllib.urlopen(api_path)
        json_data = json.loads(response.read())
    except:
        print "Error with %s" % api_path
    
    with open('./json/%s.json' % filename, 'w') as outfile:
        json.dump(json_data, outfile)

def readJSON(permalink, toPrint = False):
    filename = permalink.split('/')
    filename = filename[len(filename)-1]
    
    with open('./json/%s.json' % filename) as file:
        json_data = json.loads(file.read())

    if toPrint:
        print json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': '))

    return json_data

if __name__ == "__main__":
    #Preparing data
    keys = readAPIKeys()
    print '%d keys read' % len(keys)

    permalinks = readFetchList()
    print '%d permalinks read' % len(permalinks)
	
    log = readLog()
    print '%d log read' % len(log)

    lastUpdated, lastUpdatedDate, dailyCount = readStatus()
    print 'system status'
    print 'progress %d/%d' % (lastUpdated, len(permalinks))
    print 'lastUpdatedDate: %s' % lastUpdatedDate    

    #clean the count if it's a new day
    if lastUpdatedDate.day < datetime.now().day:
        print 'lastUpdatedDate: %s' % lastUpdatedDate
        print 'cleaning dailyCount for a new day'
        for k in dailyCount:
            dailyCount[k] = 0
        lastUpdatedDate = datetime.now()
        updateStatus(lastUpdated, lastUpdatedDate, dailyCount)

    print 'dailyCount left today:'
    for key in keys:
        print '%d for key: %s' % ((2450 - dailyCount.get(key, 0)), key)
    
    #daily routine
    for key in keys:
        print "Staring with key: %s" % key
        while dailyCount.get(key, 0) < 2450:
            try:
                fetchOneCompany(permalinks[lastUpdated], key)
            except:
                log.append(lastUpdated)
                updateLog(log)
                print lastUpdated, 'failed'

            lastUpdated += 1
            dailyCount[key] = dailyCount.get(key, 0) + 1            
            lastUpdatedDate = datetime.now()
            updateStatus(lastUpdated, lastUpdatedDate, dailyCount)

            print lastUpdated, ' files got...\r',
                
            time.sleep(1.5)
        print ""
