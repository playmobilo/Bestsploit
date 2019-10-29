from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from base import Base

class Feedback(Base):
	__tablename__ = 'feedback'
	id = Column(Integer,Sequence('feedback_id_seq'), primary_key=True)
	#TODO rename name to comment
	name = Column(String)
	exploit_id = Column(Integer,ForeignKey('exploit.id'))

	def __init__(self,name,exploit_id):
		self.name=name
		self.exploit_id = exploit_id