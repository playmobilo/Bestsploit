from sqlalchemy import Column, String, Integer, Sequence, ForeignKey, UniqueConstraint
from base import Base

class User(Base):  
	__tablename__ = 'registered_users'

	id = Column(Integer,Sequence('user_id_seq'), primary_key = True)
	username = Column(String,unique=True,nullable=False)
	password = Column(String,nullable=False)
	email = Column(String,unique=True,nullable=False)

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email
