from sqlalchemy import Column, String, Integer, Sequence, ForeignKey, UniqueConstraint
from base import Base

class ApiKeyToUser(Base):  
	__tablename__ = 'api_key_to_user'

	id = Column(Integer,Sequence('apikeytouser_id_seq'), primary_key = True)
	username = Column(String,unique=True)
	api_key = Column(String,unique=True)
	

	def __init__(self, username, apikey):
		self.username = username
		self.api_key = apikey