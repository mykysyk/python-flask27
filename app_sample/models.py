from sqlalchemy          import Table, Column, Integer, String
from app_sample.database import Base

#----------------------------------------------------------
# SAMPLE TABLE
#----------------------------------------------------------
class SampleTable(Base):

    __tablename__ = 'tbl_sample_table'

    id      = Column('id'   ,   Integer, primary_key=True)
    title   = Column('title',   String)
    message = Column('message', String,  default='default value from model')
    date    = Column('date',    String)


    def __repr__(self):
        return '<tbl_sample_table(%d, %s %s)>' % (self.id, self.title, self.message, self.date)
