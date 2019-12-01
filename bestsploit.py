import sys
import getopt
import traceback
import termcolor
import getmac
import db
import pycurl
from io import BytesIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from exploit import Exploit
from feedback import Feedback
from evaluation import Evaluation
from apikeytouser import ApiKeyToUser
USERNAME = 'Akos'
APIKEY = '614b0ea1af40826489268ce6fdac7234569810ae1a0e4b420fb810d2bf4ded72'


DATABASE = db.Db()
OPERATION = ''

#for searching
PHRASE = ''

#for upload
FILE_NAME = ''
DESC = ''
UPLOAD_PATH = 'home/akos/bme/szakdolgozat/exploit-db/exploits/Uploads'

#for adding comments
FILE_ID = ''
COMMENT = ''

#for evaluation of exploit
EVALUATION = ''
MAC_ADDRESS = 'mac'

#Download
DOWNLOAD_FILE_NAME='exploit.txt'

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'hp:u:t:i:d:g:c:e:n:')
except getopt.GetoptError:
    print('Usage: python3 bestsploit.py -h for more information.')
    #print('halo')
    sys.exit(1)

for opt, arg in OPTS:
    if opt == '-h':
        print('USAGE OF BESTSPLOIT:\n'
              '  -p "<PHRASES>": Search the given phrases in the database\n'+
              '  -d <ID>: Download the exploit with the given ID\n'+
              '  -i <ID> -c "<COMMENT>": Comment the exploit with the given ID\n'+
              '  -g <ID>: Get all the comments to the exploit with the given ID\n'+
              '  -i <ID> -e "+"/"-": Rate the exploit with the given ID.')
        sys.exit(0)

    elif opt == '-p':
        PHRASE = arg
        OPERATION = 'PHRASE'
    elif opt == '-t':
        DESC = arg
       # OPERATION = 
    elif opt == '-d':
        FILE_ID = arg
        OPERATION = 'DOWNLOAD'
    elif opt == '-i':
        FILE_ID = arg

    elif opt == '-c':
        COMMENT = arg
        OPERATION = 'COMMENT'

    elif opt == '-g':
        FILE_ID = arg
        OPERATION = 'GETCOMMENT'

    elif opt == '-e':        
        EVALUATION = arg
        OPERATION = 'EVALUATION'


if OPERATION == 'PHRASE':

    PHRASES = PHRASE.split(' ')


    EXPLOIT = DATABASE.SESSIONOBJ.query(Exploit).filter(Exploit.desc.contains(PHRASES[0])).order_by(Exploit.positive.desc()).all()
    
    FILTERED_EXPLOITS=[]
    for a in EXPLOIT:
        
        if all(x in a.desc for x in PHRASES):
            FILTERED_EXPLOITS.append(a)
    LISTA = []
    #LISTATMP = []
    if FILTERED_EXPLOITS is not []:
        for x in FILTERED_EXPLOITS:
            string = x.desc
            tmp = []
            for y in PHRASES:
                string = string.replace(y, termcolor.colored(y, 'magenta'))
                tmp = [x.id, string, x.positive, x.negative]
            
            LISTA.append(tmp)
            #LISTATMP.append(int(x.file.split(".")[0]))
    print(tabulate(LISTA, headers=["Id", "Description", "(+)", "(-)"], tablefmt="fancy_grid"))
    #print(max(LISTATMP))


if OPERATION == 'COMMENT':
    try:
        EXISTS = DATABASE.SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
        #print(EXISTS)
        
        if EXISTS is not []:
            EVAL = DATABASE.SESSIONOBJ.query(Evaluation).filter_by(exploit_id=FILE_ID,api_key=APIKEY).first()
            if EVAL is not None:

                FEEDBACK = Feedback(api_key=APIKEY, comment=COMMENT, exploit_id=FILE_ID, evaluation=EVAL.evaluation)
                DATABASE.SESSIONOBJ.add(FEEDBACK)
                DATABASE.SESSIONOBJ.commit()
            else:
                FEEDBACK = Feedback(api_key=APIKEY, comment=COMMENT, exploit_id=FILE_ID, evaluation="NOT")

                DATABASE.SESSIONOBJ.add(FEEDBACK)
                DATABASE.SESSIONOBJ.commit()
        else:
            print("There is no exploit with the id you gave!")
    except TypeError:
        traceback.print_exc()
        print('Usage: bestsploit.py -i <ID> -c <COMMENT>')
        print('Don\'t forget that ID must be an integer and the comment must be a string!')
    except:
        traceback.print_exc()
        print('Usage: bestsploit.py -i <ID> -c <COMMENT>')


if OPERATION == 'GETCOMMENT':
    try:

        E_EXPLOIT = DATABASE.SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
        LISTA = []
        #print(FI)
        if E_EXPLOIT is not None:
            E_EVALUATION = DATABASE.SESSIONOBJ.query(Evaluation).filter_by(exploit_id=E_EXPLOIT.id).all()
            E_COMMENT = DATABASE.SESSIONOBJ.query(Feedback).filter_by(exploit_id=E_EXPLOIT.id).all()
            print(E_COMMENT)
            if E_COMMENT is not None:

                for x in E_COMMENT:
                    EVALUATED_OR_NOT = 'NOT'
                    for y in E_EVALUATION:
                        if (x.api_key == y.api_key) and (x.exploit_id == y.exploit_id):
                            EVALUATED_OR_NOT = y.evaluation
                    USERAPI = DATABASE.SESSIONOBJ.query(ApiKeyToUser).filter_by(api_key=APIKEY).first()
                    tmp = [x.id, USERAPI.username, x.comment, EVALUATED_OR_NOT]
                    LISTA.append(tmp)

            else:
                print('Sorry, no comment was found to that exploit!')
        else:
            print('There is no exploit with the id you gave!')
        
        print(tabulate(LISTA, headers=["Id", "Username", "Comment", "Evaluation"], tablefmt="fancy_grid"))

    except TypeError:
        print('Usage: bestsploit.py -g <EXPLOIT_ID>')
        print('Don\'t forget that ID must be an integer!')

    except:
        traceback.print_exc()
        print('Usage: bestsploit.py -g <EXPLOIT_ID>')

if OPERATION == 'EVALUATION':
    try:
        EXISTS = False
        #átírni api-keyre!!!
        #
        EVALUATION_EXIST = DATABASE.SESSIONOBJ.query(Evaluation).filter_by(api_key=APIKEY, exploit_id=FILE_ID).all()
        for x in EVALUATION_EXIST:
            if str(x.exploit_id) == str(FILE_ID):
                EXISTS = True
        if EXISTS == False:
    
            EXPLOIT = DATABASE.SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
            UPDATE_FEEDBACK = DATABASE.SESSIONOBJ.query(Feedback).filter_by(api_key=APIKEY, exploit_id=FILE_ID).all()
            #print(len(UPDATE_FEEDBACK))
            if len(UPDATE_FEEDBACK) >0:
                #print('IGEN')
                #UPDATE_EVALUATION = DATABASE.SESSIONOBJ.query(Evaluation).filter_by(api_key=APIKEY, exploit_id=FILE_ID).all()
                for x in EVALUATION_EXIST:
                    
                    x.evaluation = EVALUATION
            
            if EVALUATION == '+':
                EXPLOIT.positive += 1
                EVALUATION = Evaluation(APIKEY, FILE_ID,'+') 
                DATABASE.SESSIONOBJ.add(EVALUATION)
                DATABASE.SESSIONOBJ.commit()
            
            elif EVALUATION == '-':
                EXPLOIT.negative -= 1
                EVALUATION = Evaluation(APIKEY, FILE_ID,'-') 
                DATABASE.SESSIONOBJ.add(EVALUATION)
                DATABASE.SESSIONOBJ.commit()
            else:
                print('Wrong parameters!')
        else:
            print('You have already evaluated the exploit you gave!')
    except:
        traceback.print_exc()
        print('Usage: bestsploit.py -i <EXPLOIT_ID> -e \'+\'/\'-\'')


if OPERATION == 'DOWNLOAD':
    #print('------------------------'+FILE_ID)

    EXISTS = DATABASE.SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
   # print(EXISTS)
    if EXISTS is not []:
        
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'localhost:8000'+EXISTS.path)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        body = buffer.getvalue()
        file = open(EXISTS.file, "w") 
        file.write(body.decode('iso-8859-1')) 
        file.close()
        #print(body.decode('iso-8859-1'))
    else:
        traceback.print_exc()
        print('There is no exploit with the given ID. Please try again.')
#MAC cím alapján biztosítom hogy ne adhasson több értékelést egy adott exploitra
#fail to ban dos ellen
#dátum alapján elmentem hogy mikor frissítettem utoljára és csak-int-é alakítani és működik.