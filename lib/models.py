from sqlalchemy import ForeignKey, Column, Integer, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


engine = create_engine('sqlite:///your_database.db')  
Session = sessionmaker(bind=engine)
session = Session()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(dev=dev, company=self, item_name=item_name, value=value)
        session.add(new_freebie)  
        session.commit()  
        return new_freebie

    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()

    freebies = relationship('Freebie', backref='company')
    devs = relationship('Dev', secondary='freebies')

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
            session.commit()  

    freebies = relationship('Freebie', backref='dev')
    companies = relationship('Company', secondary='freebies')

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    dev_id = Column(Integer(), ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"


Base.metadata.create_all(engine)
