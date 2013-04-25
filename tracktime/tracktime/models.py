from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                        expire_on_commit=False))
Base = declarative_base()


class TrackTimeEntry(Base):
    __tablename__ = 'tracktime'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime(), default=datetime.now)
    stop_time = Column(DateTime(), nullable=True)
    msg = Column(Text)
