import sys, getopt
from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker

from exploit import Exploit
from feedback import Feedback
from base import Base


operation = ''
phrase=''
file_name = ''
ofile_name = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hedp:i:o:')
except getopt.GetoptError:
    print('Usage: bestsploit.py -p <phrase>')
    sys.exit(1)

for opt, arg in opts:
    if opt == '-h':
        print('Usage: bestsploit.py -p <phrase>')
        sys.exit(0)
    elif opt == '-p':
        phrase = arg
        operation = '-p'    
if operation == '-p':
    db_string = 'postgres://admin:19970707@localhost:5432/Bestsploit'
    engine = create_engine(db_string)
    Session = sessionmaker(engine)  
    session = Session()
    Exploit = session.query(Exploit).filter_by(file=phrase).first()
    print(Exploit.path)
     