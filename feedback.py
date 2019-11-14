from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from base import Base

class Feedback(Base):
	__tablename__ = 'feedback'
	id = Column(Integer,Sequence('feedback_id_seq'), primary_key=True)
	username = Column(String)
	comment = Column(String)
	exploit_id = Column(Integer,ForeignKey('exploit.id'))
	evaluation = Column(Integer)

	def __init__(self,username,comment,exploit_id,evaluation):
		self.username = username
		self.comment = comment
		self.exploit_id = exploit_id
		self.evaluation = evaluation