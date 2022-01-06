from gpapi.googleplay import GooglePlayAPI
from getpass import getpass
import csv, os, subprocess, logging, sys, getopt, tempfile, shutil

argumentList = sys.argv[1:]
options = "f:l:L:m:d:T:t:g:h"
long_options = ["filename", "logname", "Locale", "mail", "token", "help", "device", "Timezone", "gsfID"]
logname = ""
path = ""
locale = "en_US"
mail = ""
passwd = ""
token = ""
timezone="UTC"
device= "hero2lte"
gsfID = 0

def printHelp():
    print("""-h, --help: Print current help
            -f, --filename (REQUIRED): file path to app ID list
            -l, --logname (REQUIRED): logname for logfile
            -L, --Locale (optional): set locale when initializing, standard is "en_US"
            -T, --Timezone (optional): timezone to use, standard is "UTC"
            -d, --device (optional): device codename to use, standard: "hero2lte

            Either (token AND gsfId) or mail are REQUIRED:
            -t, --token: set token to use instead of login
            -g, --gsfID: set gsfID to use instead of login
            
            -m, --mail: mail for login
    """)

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--help"):
            printHelp()
            exit()
        elif currentArgument in ("-f", "--filename"):
            path = currentValue
        elif currentArgument in ("-l", "--logname"):
            logname = currentValue
        elif currentArgument in ("-L", "--Locale"):
            locale = currentValue
        elif currentArgument in ("-m", "--mail"):
            mail = currentValue
            print("Please enter your Google Account password: ")
            passwd = getpass()
        elif currentArgument in ("-t", "--token"):
            token = currentValue
        elif currentArgument in ("-T", "--Timezone"):
            timezone = currentValue
        elif currentArgument in ("-d", "--device"):
            device = currentValue
        elif currentArgument in ("-g", "--gsfID"):
            gsfID = int(currentValue)

except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

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

api = GooglePlayAPI(locale=locale, timezone=timezone, device_codename=device)

if mail:
    api.login(email=mail, password=passwd)
    if hasattr(api,"authSubToken"):
        logger.info("Login successfully, you may want to use the following token and gsfID in the future to prevent initializing a new device with each login: ")
        logger.info("-t "+api.authSubToken+" -m "+str(api.gsfId))
    else:
        logger.error("Login failed!")
        exit()
elif token and gsfID:
    api.login(authSubToken=token, gsfId=gsfID)
else:
    logger.error("You need to enter either a token (-t, --token) AND gsfId (-g, --gsfId) or ONLY a mail (-m, --mail)!")
    printHelp()
    exit()


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
        tempdir = tempfile.mkdtemp()
        iteration+=1
        print("Iteration: "+str(iteration))
        docid = line[0]
        try:
            download = api.download(docid, expansion_files=True)
            with open(tempdir+"/"+download['docId'] + '.apk', 'wb') as first:
                for chunk in download.get('file').get('data'):
                    first.write(chunk)
        except:
            logger.error("Failed to download "+docid)
            continue

        if(download['docId'] + '.apk' in os.listdir(tempdir)):
            downloadedApps+=1
            process = subprocess.Popen("unzip -o " +tempdir+"/"+download['docId'] + '.apk'+" -d "+tempdir+"/"+download['docId'], shell=True)
            out, err = process.communicate()
            process.wait()
            if(process.returncode == -1 or not download['docId'] in os.listdir(tempdir)):
                logger.error("Failed to unzip: "+download['docId']+'.apk')
                continue
            else:
                pathToUse = "'{path}/{docid}'".format(path = tempdir, docid=download['docId'])
                process = subprocess.Popen("grep -rnw "+pathToUse+" -e 'NotificationCompat' -e'onMessageReceived'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.wait()
                out, err = process.communicate()
                out+=err
                try:
                    process.kill()
                except OSError:
                    # can't kill a dead proc
                    pass
                #Wenn NotificationCompat vorhanden ist, kann die App Push Notifications empfangen und zählt somit zu der gesamten Anzahl
                if b'onMessageReceived' in out or b'matches' in out or b'NotificationCompat' in out:
                    appsWithPush+=1
                    process = subprocess.Popen("grep -rnw "+pathToUse+" -e 'Capillary' -e 'capillary'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    #Es wird der Buffer vor dem wait geleert, da der Prozess sonst hängen bleibt, weil er darauf wartet dass der Buffer geleert wird.
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

                shutil.rmtree(tempdir)
                logger.info("Iteration: "+str(iteration)+" downloadedApps: "+str(downloadedApps)+" appsWithPush: "+str(appsWithPush)+" withCapillary: "+str(withCapillary)+  " withXmpp: "+ str(withXmpp))
        else:
            logger.error("Download failed for: "+download['docId'] + '.apk')

