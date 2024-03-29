from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker
from exploit import Exploit
from feedback import Feedback
from evaluation import Evaluation
from base import Base
import glob
import git 
import apikeytouser
import getpass
from user import User
from apikeytouser import ApiKeyToUser
import traceback

PATH = '/home/akos/bme/szakdolgozat/exploit-db/'
files = [f for f in glob.glob(PATH + "**/*.*", recursive=True)]

class Db():

	db_string = 'postgres://admin:19970707@localhost:5432/Bestsploit'
	engine = create_engine(db_string)
	Session = sessionmaker(engine)  
	SESSIONOBJ = Session()


	def delete(self):

		Base.metadata.drop_all(bind=self.engine, tables=[ApiKeyToUser.__table__])
		Base.metadata.drop_all(bind=self.engine, tables=[User.__table__])
		Base.metadata.drop_all(bind=self.engine, tables=[Evaluation.__table__])
		Base.metadata.drop_all(bind=self.engine, tables=[Feedback.__table__])
		Base.metadata.drop_all(bind=self.engine, tables=[Exploit.__table__])

	def add(self,max_number):

		for f in files:
			tolist = f.split('/')

			file_name = tolist[len(tolist)-1]
			#print(file_name)
			try:
				file_name_to_number = int(file_name.split(".")[0])

				if max_number != 0:
					if int(file_name_to_number)>max_number:
						
						file_path = f
						file_title = self.set_description(file_name)
						print(file_title)
						if file_title is not None:
							exploit = Exploit(file_name,file_title,file_path,0,0)
							self.SESSIONOBJ.merge(exploit)
							print(exploit.file)	
						else:
							print('DESC NOT FOUND')
				else:
					file_path = f
					file_title = self.set_description(file_name)
					print(file_title)
					if file_title is not None:
						exploit = Exploit(file_name,file_title,file_path,0,0)
						self.SESSIONOBJ.add(exploit)
						print(exploit.file)	
					else:
							print('DESC NOT FOUND')	
			except:
				print('NEM SZAM')
		self.SESSIONOBJ.commit()
	
	def create(self):
		Base.metadata.create_all(self.engine)

	def set_description(self,exploit_name):
		with open('/home/akos/bme/szakdolgozat/exploit-db/files_exploits.csv','r') as file:
			for line in file:
				txt = line.split(',') 
				txt1 = txt[1].split('/')

				if exploit_name == txt1[len(txt1)-1]:
					
					return txt[2]

		return None

	def update(self):

		LISTATMP = []
		
		for f in files:
			tolist = f.split('/')
			file_name = tolist[len(tolist)-1]
			try:
				LISTATMP.append(int(file_name.split(".")[0]))

			except Exception as e:
				print('Nem szam')
		MAX_NUMBER = max(LISTATMP)


		g = git.cmd.Git('~/bme/szakdolgozat/exploit-db/')
		g.pull()

		self.add(MAX_NUMBER)
		print(MAX_NUMBER)



	def new_api_key(self, api_key, username):
		try:
			EXISTS = self.SESSIONOBJ.query(User).filter_by(username=username).first()
			PASSWORD = getpass.getpass()
			print(EXISTS)
			if EXISTS is not None:
				if PASSWORD is not None and PASSWORD == EXISTS.password:
					API_KEY_USER_DELETE = self.SESSIONOBJ.query(ApiKeyToUser).filter_by(username=username).first()
					print(API_KEY_USER_DELETE)
					if API_KEY_USER_DELETE is not None:
						self.SESSIONOBJ.delete(API_KEY_USER_DELETE)
						NEW_KEY_TO_USER = ApiKeyToUser(username,api_key)
						self.SESSIONOBJ.add(NEW_KEY_TO_USER)
						self.SESSIONOBJ.commit()
						print('New Api Key was created! Please place it in the bestsploit.py to the correct place.\nYour api key is:'+api_key)
					else:
						if PASSWORD == EXISTS.password and PASSWORD is not None:
							NEW_KEY_TO_USER = ApiKeyToUser(username,api_key)
							self.SESSIONOBJ.add(NEW_KEY_TO_USER)
							self.SESSIONOBJ.commit()
							print('Api Key was created! Please place it in the bestsploit.py to the correct place.\nYour api key is:'+api_key)
						else:
							print('New is created')
						
				else:
					print("wrong credentials!")
					
			else:
				print('There is no user with that username!')
		except NoneType:
			traceback.print_exc()
			print('Exception happened')

	def register(self, username, password, email):
		try:
			EXISTS = self.SESSIONOBJ.query(User).filter_by(username=username).first()
			if EXISTS is not None:
				print('The chosen username is already taken. Please, try again with another one!')
			else:
				NEW_USER = User(username,password,email)
				self.SESSIONOBJ.add(NEW_USER)
				self.SESSIONOBJ.commit()
		except:
			traceback.print_exc()
			print('An exception happened during registration')

#def main():
#
#	db = Db()
#	#db.update()
#
#	#db.delete()
#	#db.create()
#	#db.add(0)
#
#	print('done')
#main()




