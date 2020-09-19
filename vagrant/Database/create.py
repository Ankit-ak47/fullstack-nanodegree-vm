from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()
'''mySecondRestaurant=Restaurant(name="Pizza Palace")
session.add(mySecondRestaurant)
session.commit()'''
print(session.query(Restaurant).all())
#for updating simple use 'Classname.attribute'=value
#session.delete(Class Name) 
