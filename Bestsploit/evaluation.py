from sqlalchemy import Column, String, Integer, Sequence, ForeignKey, UniqueConstraint
from base import Base

class Evaluation(Base):  
	__tablename__ = 'evaluation'

	id = Column(Integer,Sequence('evaluation_id_seq'), primary_key = True)
	api_key = Column(String)
	exploit_id = Column(Integer, ForeignKey('exploit.id'))
	evaluation = Column(String)
	def __init__(self, api_key, exploit_id, evaluation):
		self.api_key = api_key
		self.exploit_id = exploit_id
		self.evaluation = evaluation

