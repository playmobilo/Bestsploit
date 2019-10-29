from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker
from exploit import Exploit
from feedback import Feedback
from base import Base
import glob

class Cron(base):
	db_string = 'postgres://admin:19970707@localhost:5432/Bestsploit'
	engine = create_engine(db_string)
	Session = sessionmaker(engine)  
	session = Session()

	def update(self):
		
