from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
from random_word import RandomWords
engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()
# mySecondRestaurant=Restaurant(name="Pizza Palace")
# session.add(mySecondRestaurant)
# session.commit()
j=1
# for i in session.query(MenuItem).all():
#     session.delete(i)
#     session.commit()
#     j+=1
print([i for i in (session.query(MenuItem))])
pizzadup=session.query(Restaurant).filter_by(id=3).one()
print(pizzadup.name)
# session.delete(pizzadup)
# session.commit()
# #for updating simple use 'Classname.attribute'=value
#session.delete(Class Name)
#session.rollback()
#session.rollback()