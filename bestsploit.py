import sys
import getopt
import traceback
import termcolor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from exploit import Exploit
from feedback import Feedback

DB_STRING = 'postgres://admin:19970707@localhost:5432/Bestsploit'
ENGINE = create_engine(DB_STRING)
SESSION = sessionmaker(ENGINE)
SESSIONOBJ = SESSION()

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

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'hp:u:t:d:i:c:g:e:n:')
except getopt.GetoptError:
    print('Usage: bestsploit.py -p <PHRASE>')
    sys.exit(1)

for opt, arg in OPTS:

    if opt == '-h':
        print('Usage: bestsploit.py -p <PHRASE>')
        sys.exit(0)

    elif opt == '-p':
        PHRASE = arg
        OPERATION = 'PHRASE'

    elif opt == '-u':
        FILE_NAME = arg
        OPERATION = 'UPLOAD'
    elif opt == '-t':
        DESC = arg
       # OPERATION = 

    elif opt == '-d':
        FILE_NAME = arg
        OPERATION = 'DELETE'

    elif opt == '-i':
        FILE_ID = arg

    elif opt == '-c':
        COMMENT = arg
        OPERATION = 'COMMENT'

    elif opt == '-g':
        FILE_ID = arg
        OPERATION = 'GETCOMMENT'

    elif opt == '-e':
        if arg != 1 or arg != -1:
            print('Wrong value to EVALUATION')
        else:
            EVALUATION = arg
            OPERATION = 'EVALUATE'


if OPERATION == 'PHRASE':

    EXPLOIT = SESSIONOBJ.query(Exploit).filter(Exploit.desc.contains(PHRASE)).all()

    LISTA = []
    LISTATMP = []
    if EXPLOIT is not []:
        for x in EXPLOIT:
            string = x.desc
            string = string.replace(PHRASE, termcolor.colored(PHRASE, 'magenta'))
            tmp = [x.id, string, x.positive, x.negative]
            LISTA.append(tmp)
            LISTATMP.append(int(x.file.split(".")[0]))

    
    print(tabulate(LISTA, headers=["Id", "Description", "(+)", "(-)"], tablefmt="fancy_grid"))
    print(max(LISTATMP))
if OPERATION == 'UPLOAD':

    try:
        EXISTS = SESSIONOBJ.query(Exploit).filter_by(file=FILE_NAME).all()
        if EXISTS == []:

            EXPLOIT = Exploit(file=FILE_NAME, desc=DESC, path=UPLOAD_PATH, positive=0, negative=0)
            SESSIONOBJ.add(EXPLOIT)
            SESSIONOBJ.commit()
        else:
            print('File name already exists! Try again with another name!')

        print('UPLOAD')
        print(EXISTS)
    except:
        print('Usage: bestsploit.py -u <FILENAME> -t <DESCRIPTION>')



#TODO delete from production!!!
if OPERATION == 'DELETE':

    EXISTS = SESSIONOBJ.query(Exploit).filter_by(file=FILE_NAME).all()
    print(EXISTS)
    if EXISTS is not []:
        SESSIONOBJ.delete(EXISTS[0])
        SESSIONOBJ.commit()


if OPERATION == 'COMMENT':
    try:
        EXISTS = SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
        print(EXISTS)
        
        if EXISTS is not []:
            FEEDBACK = Feedback(name=COMMENT, exploit_id=FILE_ID)
            SESSIONOBJ.add(FEEDBACK)
            SESSIONOBJ.commit()
        else:
            print("There is no exploit with the id you gave!")
    except:
        print('Usage: bestsploit.py -i <ID> -c <COMMENT>')


if OPERATION == 'GETCOMMENT':
    try:
        E_EXPLOIT = SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()
        LISTA = []

        if E_EXPLOIT is not []:

            E_COMMENT = SESSIONOBJ.query(Feedback).filter_by(exploit_id=E_EXPLOIT.id).all()
            if E_COMMENT is not []:
                for x in E_COMMENT:
                    tmp = [x.id, x.name]
                    LISTA.append(tmp)

            else:
                print('Sorry, no comment was found to that exploit!')
        else:
            print('There is no exploit with the id you gave!')
        
        print(tabulate(LISTA, headers=["Id", "name"], tablefmt="fancy_grid"))


    except:
        traceback.print_exc()
        print('Usage: bestsploit.py -g <EXPLOIT_ID>')

#if OPERATION == 'EVALUATION':
 #   try:
  #      E_EXPLOIT = SESSIONOBJ.query(Exploit).filter_by(id=FILE_ID).first()

   #     if E_EXPLOIT is not []:
            

#MAC cím alapján biztosítom hogy ne adhasson több értékelést egy adott exploitra
#fail to ban dos ellen
