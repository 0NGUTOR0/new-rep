from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
class Post( Base ):
    __tablename__ = "SQLALCHEMY POSTS"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable= False)
    Published = Column(Boolean, server_default="TRUE", nullable=False)
    Created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    Poster = Column(Integer, ForeignKey("SQLALCHEMY USERS.id", ondelete= "CASCADE"), nullable=False)
    
    Owner = relationship("Users")

class Users( Base ):
    __tablename__ = "SQLALCHEMY USERS"

    Name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, )
    id = Column(Integer, primary_key=True, nullable=False)
    Created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Likes(Base):
    __tablename__ = "LIKES"
    post_id = Column(Integer, ForeignKey("SQLALCHEMY POSTS.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("SQLALCHEMY USERS.id", ondelete="CASCADE"), nullable=False, primary_key=True)


class Follows(Base):
    __tablename__= "FOLLOWS"
    leaders= Column(Integer, ForeignKey("SQLALCHEMY USERS.id",ondelete= "CASCADE"), nullable=False, primary_key=True)
    followers= Column(Integer, ForeignKey("SQLALCHEMY USERS.id",ondelete= "CASCADE"), nullable=False, primary_key=True)               