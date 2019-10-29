from sqlalchemy import Column, String, Integer, Sequence, ForeignKey, UniqueConstraint
from base import Base

class Evaluation(Base):  
	__tablename__ = 'evaluation'

	id = Column(Integer,Sequence('evaluation_id_seq'), primary_key = True)
	mac_address = Column(String, unique=True)
	exploit_id = Column(Integer, ForeignKey('exploit.id'))
	def __init__(self, mac_address, exploit_id):
		self.mac_address = mac_address
		self.exploit_id = exploit_id

	def __repr__(self):
		json = str('['+self.id+', '+self.mac_address+']')
		return json
