from sqlalchemy                 import create_engine
from sqlalchemy.orm             import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.interfaces      import PoolListener

#----------------------------------------------------------
# CONFIG
#----------------------------------------------------------
import config
_SQLITE3 = config.app_sample.SQLITE3

#----------------------------------------------------------
# CREATE ENGINE
#----------------------------------------------------------
engine = create_engine('sqlite:///' + _SQLITE3,
                        convert_unicode = True,
                        echo            = False)

db_session = scoped_session(sessionmaker(autocommit = False,
                                         autoflush  = False,
                                         bind       = engine))

Base       = declarative_base()
Base.query = db_session.query_property()

#----------------------------------------------------------
# DB INIT
# python -c "from app_sample.database import init_db;init_db()"
#----------------------------------------------------------
def init_db():

    import app_sample.models
    Base.metadata.create_all(bind=engine)
