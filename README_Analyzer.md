Dependencies:
https://github.com/TheZ3ro/googleplay-api/tree/patch-1

requests 2.20.0


Options:
-h, --help: Print current help

-f, --filename (REQUIRED): file path to app ID list

-l, --logname (REQUIRED): logname for logfile

-L, --Locale (optional): set locale when initializing, standard is "en_US"

-T, --Timezone (optional): timezone to use, standard is "UTC"

-d, --device (optional): device codename to use, standard: "hero2lte

Either (token AND gsfId) or mail are REQUIRED:

-t, --token: set token to use instead of login

-g, --gsfID: set gsfID to use instead of login
            
-m, --mail: mail for login

Filelist needs linebreak as seperator, example:

com.testapp

com.apptest

Example command:

python analyzer.py -f my/path/file.txt -l logfile.log -m myemail.gmail.com
