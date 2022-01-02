from gpapi.googleplay import GooglePlayAPI
import csv, os, subprocess, logging, sys, getopt

argumentList = sys.argv[1:]
options = "f:l:"
long_options = ["filename", "logname"]
logname = ""
path = ""
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-f", "--filename"):
            path = currentValue
             
        elif currentArgument in ("-l", "--logname"):
            logname = currentValue
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

#mail = "hbrsprojektinf@gmail.com"
#mail = "hbibissam91@gmail.com"
#passwd = "Hbrs1234%"
#passwd = "zislspevpxgaopwj"
api = GooglePlayAPI(locale="en_US", timezone="UTC", device_codename="hero2lte")
#requests 2.20.0 needed
#api.login(email=mail, password=passwd)
api.login(authSubToken='FAgO4ipcn9zfZkr1_-oUwSHy6G_97Zvi0jmbjHacZOSFkyT_sIb6m3JcY562sNNkoquOEQ.', gsfId=4340149443977775908)

###Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(logname)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

downloadedApps = 0
appsWithPush = 0
withCapillary = 0
withMqtt = 0
withXmpp = 0
iteration = 0

###Analyzer
with open(path, "r") as file:
    reader = csv.reader(file)
    for idx,line in enumerate(reader):
        iteration+=1
        print("Iteration: "+str(iteration))
        docid = line[0]
        os.makedirs(os.getcwd()+"/tmp", exist_ok=True)
        try:
            download = api.download(docid, expansion_files=True)
            with open('tmp/'+download['docId'] + '.apk', 'wb') as first:
                for chunk in download.get('file').get('data'):
                    first.write(chunk)
        except:
            logger.error("Failed to download "+docid)
            continue

        if(download['docId'] + '.apk' in os.listdir('tmp')):
            downloadedApps+=1
            process = subprocess.Popen("unzip -o " +os.getcwd()+"/tmp/"+download['docId'] + '.apk'+" -d "+os.getcwd()+"/tmp/"+download['docId'], shell=True)
            out, err = process.communicate()
            process.wait()
            if(process.returncode == -1 or not download['docId'] in os.listdir('tmp/')):
                logger.error("Failed to unzip: "+download['docId']+'.apk')
                continue
            else:
                pathToUse = "'{path}/tmp/{docid}'".format(path = os.getcwd(), docid=download['docId'])
                process = subprocess.Popen("grep -rnw "+pathToUse+" -e 'NotificationCompat'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.wait()
                out, err = process.communicate()
                out+=err
                try:
                    process.kill()
                except OSError:
                    # can't kill a dead proc
                    pass
                #Wenn NotificationCompat vorhanden ist, kann die App Push Notifications erstellen und zählt somit zu der gesamten Anzahl
                if b'NotificationCompat' in out or b'matches' in out:
                    appsWithPush+=1
                    process = subprocess.Popen("grep -rnw "+pathToUse+" -e 'Capillary' -e 'capillary'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = process.communicate()
                    out+=err
                    process.wait()
                    tmp = process.communicate()
                    out += tmp[0]
                    out += tmp[1]

                    try:
                        process.kill()
                    except OSError:
                        # can't kill a dead proc
                        pass
                    if b'Capillary' in out or b'capillary' in out or b'matches' in out or b'xmpp' in out or b'XMPP' in out:
                        withCapillary+=1
                        logger.info(download['docId']+" has capillary")

                ######
                    process = subprocess.Popen("grep -rnw "+pathToUse+" -e 'xmpp' -e 'XMPP'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = process.communicate()
                    out+=err
                    process.wait()
                    tmpout, tmperr = process.communicate()
                    out+=tmpout
                    out+=tmperr
                    try:
                        process.kill()
                    except OSError:
                        # can't kill a dead proc
                        pass
                    if  b'matches' in out or b'xmpp' in out or b'XMPP' in out:
                        withXmpp+=1
                        logger.info(download['docId']+" has xmpp")

                #####
                #Dieser Command ist gefährlich
                process = subprocess.Popen("rm -rf "+pathToUse+"*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.wait()
                try:
                    process.kill()
                except OSError:
                    # can't kill a dead proc
                    pass
                logger.info("Iteration: "+str(iteration)+" downloadedApps: "+str(downloadedApps)+" appsWithPush: "+str(appsWithPush)+" withCapillary: "+str(withCapillary)+  " withXmpp: "+ str(withXmpp))
        else:
            logger.error("Download failed for: "+download['docId'] + '.apk')
        


