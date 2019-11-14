from sqlalchemy import Column, String, Integer, Sequence, ForeignKey, UniqueConstraint
from base import Base

class Evaluation(Base):  
	__tablename__ = 'evaluation'

	id = Column(Integer,Sequence('evaluation_id_seq'), primary_key = True)
	username = Column(String,unique=True)
	exploit_id = Column(Integer, ForeignKey('exploit.id'))
	evaluation = Column(String)
	def __init__(self, username, exploit_id, evaluation):
		self.username = username
		self.exploit_id = exploit_id
		self.evaluation = evaluation

