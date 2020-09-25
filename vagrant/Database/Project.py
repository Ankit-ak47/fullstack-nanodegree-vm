from flask import Flask,render_template,request,url_for,redirect,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant=restaurant,items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method=="POST":
        newMenu=MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(newMenu)
        session.commit()
        flash("new menu item created!!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    return render_template('newmenuitem.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    # restaurant=session.query(Restaurant).filter_by(restaurant_id=restaurant_id)

    editedname = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        if request.form['name']:
            editedname.name=request.form['name']
            session.add(editedname)
            session.commit()
            flash("menu name updated !!!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id,items=editedname)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteditem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        session.delete(deleteditem)
        session.commit()
        flash("Item Deleted !!!!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    return render_template('deletemenuitem.html',item=deleteditem)
@app.route("/restaurants/<int:restaurant_id>/JSON/")
def restaurantMenuJSON(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItem=[i.serialize for i in items])

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/")
def menuItemJSON(restaurant_id,menu_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant.id,id=menu_id)
    return jsonify(MenuItem=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key="super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=8080)