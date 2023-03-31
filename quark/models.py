from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from quark.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id"))

    tasks = relationship("Task", back_populates="chat")


class ChatMember(Base):
    __tablename__ = "chat_members"

    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class ChatMesssage(Base):
    __tablename__ = "chats_messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)


class Org(Base):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    tel = Column(String, unique=True)
    address = Column(String, unique=True)

    users = relationship("User", back_populates="org")
    tasks = relationship("Task", back_populates="org")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    patronymic = Column(String)
    tel = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    org_id = Column(Integer, ForeignKey("orgs.id"))
    type_id = Column(Integer, ForeignKey("user_types.id"))

    customer = relationship("Customer", back_populates="user", uselist=False)
    performer = relationship("Performer", back_populates="user", uselist=False)
    org = relationship("Org", back_populates="users")
    type = relationship("UserType", back_populates="user")


class Customer(Base):
    __tablename__ = "customers"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    workspace = Column(String, unique=True)

    user = relationship("User", back_populates="customer")
    tasks = relationship("Task", back_populates="customer")
    archive = relationship("Archive", back_populates="customer")


class Performer(Base):
    __tablename__ = "performers"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group = Column(String)

    user = relationship("User", back_populates="performer")
    tasks = relationship("Task", back_populates="performer")
    archive = relationship("Archive", back_populates="performer")


class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    tasks = relationship("Task", back_populates="states")
    archive = relationship("Archive", back_populates="states")


class UserType(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    user = relationship("User", back_populates="type")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    archive = relationship("Archive", back_populates="tag")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    workplace = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.user_id"))
    performer_id = Column(Integer, ForeignKey("performers.user_id"))
    state_id = Column(Integer, ForeignKey("states.id"))
    description = Column(String)
    files = Column(String)
    history = Column(String)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    org_id = Column(Integer, ForeignKey("orgs.id"))
    time_start = Column(TIMESTAMP)
    time_end = Column(TIMESTAMP)

    customer = relationship("Customer", back_populates="tasks")
    performer = relationship("Performer", back_populates="tasks")
    states = relationship("State", back_populates="tasks")
    chat = relationship("Chat", back_populates="tasks")
    org = relationship("Org", back_populates="tasks")


class Archive(Base):
    __tablename__ = "archive"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    customer_id = Column(Integer, ForeignKey("customers.user_id"))
    workspace = Column(String)
    performer_id = Column(Integer, ForeignKey("performers.user_id"))
    status_id = Column(Integer, ForeignKey("states.id"))
    description = Column(String)
    history = Column(String)
    chat = Column(String)
    files = Column(String)
    time_start = Column(TIMESTAMP)
    time_end = Column(TIMESTAMP)
    tag_id = Column(Integer, ForeignKey("tags.id"))

    customer = relationship("Customer", back_populates="archive")
    performer = relationship("Performer", back_populates="archive")
    states = relationship("State", back_populates="archive")
    tag = relationship("Tag", back_populates="archive")
