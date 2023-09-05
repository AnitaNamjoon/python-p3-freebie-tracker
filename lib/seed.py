#!/usr/bin/env python3

#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie


engine = create_engine('sqlite:///freebies.db')


Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    
    company1 = Company(name='Company A', founding_year=2000)
    company2 = Company(name='Company B', founding_year=1995)
    company3 = Company(name='Company C', founding_year=2010)

    
    dev1 = Dev(name='Dev X')
    dev2 = Dev(name='Dev Y')
    dev3 = Dev(name='Dev Z')

    
    session.add_all([company1, company2, company3, dev1, dev2, dev3])
    session.commit()

    
    company1.give_freebie(dev1, 'Item 1', 50)
    company1.give_freebie(dev2, 'Item 2', 30)
    company2.give_freebie(dev1, 'Item 3', 40)
    company3.give_freebie(dev3, 'Item 4', 20)

if __name__ == '__main__':
    seed_data()

