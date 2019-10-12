from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker

from exploit import Exploit
from feedback import Feedback
from base import Base

import glob


PATH = '/home/akos/bme/Bestsploit/Code/'
files = [f for f in glob.glob(PATH + "**/*.*", recursive=True)]

class Db():

	db_string = 'postgres://admin:19970707@localhost:5432/Bestsploit'
	engine = create_engine(db_string)
	Session = sessionmaker(engine)  
	session = Session()

	def delete(self):
		Base.metadata.drop_all(bind=self.engine, tables=[Feedback.__table__])
		Base.metadata.drop_all(bind=self.engine, tables=[Exploit.__table__])


	def add(self):

		for f in files:
			tolist = f.split('/')
			file = tolist[len(tolist)-1]
			exists = self.session.query(Exploit).filter_by(name=file).first()
			if not exists:
				exploit = Exploit(file,1,1)
				print (f)
				self.session.merge(exploit)
			
		
		#id = self.session.query(Exploit).filter_by(name="cucc1").first()
		#print(id.id)
		#feedback = Feedback('name1',id.id)
		#self.session.add(feedback)
		self.session.commit()


	def create(self):
		Base.metadata.create_all(self.engine)


db = Db()
#db.delete()
#db.create()

db.add()

print('done')

#

#exploit = session.query(Exploit).get(1)

#session.delete(exploit)


