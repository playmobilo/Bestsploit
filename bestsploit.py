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

USERNAME = 'Akos'
APIKEY = 'N2hr5ipHF_QV-ChdJUkLeX8McAs301e9-Cc-d3xg'

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
    print('Usage: bestsploit.py -p <PHRASE>')
    print('halo')
    sys.exit(1)

for opt, arg in OPTS:
    if opt == '-h':
        print('Usage: bestsploit.py -p <PHRASE>')
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

    EXPLOIT = DATABASE.SESSIONOBJ.query(Exploit).filter(Exploit.desc.contains(PHRASE)).order_by(Exploit.positive.desc()).all()

    LISTA = []
    #LISTATMP = []
    if EXPLOIT is not []:
        for x in EXPLOIT:
            string = x.desc
            string = string.replace(PHRASE, termcolor.colored(PHRASE, 'magenta'))
            tmp = [x.id, string, x.positive, x.negative]
            LISTA.append(tmp)
            #LISTATMP.append(int(x.file.split(".")[0]))

    
    print(tabulate(LISTA, headers=["Id", "Description", "(+)", "(-)"], tablefmt="fancy_grid"))
    #print(max(LISTATMP))


if OPERATION == 'COMMENT':
    try:
        EXISTS = DATABASE.SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
        print(EXISTS)
        
        if EXISTS is not []:
            print('EVAL ELŐTT')
            EVAL = DATABASE.SESSIONOBJ.query(Evaluation).filter_by(exploit_id=FILE_ID).filter_by(username=USERNAME).all()
            print('KUTYA)')
            if EVAL is not []:
                print('eval is none')
                print(USERNAME)
                FEEDBACK = Feedback(username=USERNAME, comment=COMMENT, exploit_id=FILE_ID, evaluation=0)
                DATABASE.SESSIONOBJ.add(FEEDBACK)
                DATABASE.SESSIONOBJ.commit()
            else:
                print('eval is not none')
                FEEDBACK = Feedback(username=USERNAME, comment=COMMENT, exploit_id=FILE_ID, evaluation=1)

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
            if E_COMMENT is not None:

                for x in E_COMMENT:
                    EVALUATED_OR_NOT = 'NOT'
                    for y in E_EVALUATION:
                        if x.username == y.username:
                            EVALUATED_OR_NOT = y.evaluation
                    tmp = [x.id, x.username, x.comment, EVALUATED_OR_NOT]
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
        #traceback.print_exc()
        print('Usage: bestsploit.py -g <EXPLOIT_ID>')

if OPERATION == 'EVALUATION':
    try:
        EXISTS = False
        EVALUATION_EXIST = DATABASE.SESSIONOBJ.query(Evaluation).filter_by(username=USERNAME)
        for x in EVALUATION_EXIST:
            if x.exploit_id == FILE_ID:
                EXISTS = True
        if EXISTS == False:
    
            EXPLOIT = DATABASE.SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
            
            if EVALUATION == '+':
                EXPLOIT.positive += 1
                EVALUATION = Evaluation(USERNAME, FILE_ID,'+') 
                DATABASE.SESSIONOBJ.add(EVALUATION)
                DATABASE.SESSIONOBJ.commit()
            
            elif EVALUATION == '-':
                EXPLOIT.negative -= 1
                EVALUATION = Evaluation(MAC_ADDRESS, FILE_ID,'-') 
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
    print('------------------------'+FILE_ID)

    EXISTS = DATABASE.SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
    print(EXISTS)
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