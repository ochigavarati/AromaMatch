from ext import db
from app import app
from models import User, Comment, Product
from app import app
from ext import db
from models import User, Product


with app.app_context():
    print("მონაცემთა ბაზის ცხრილები იქმნება...")
    db.create_all()
    print("ბაზა წარმატებით განახლდა და შეიქმნა! 🚀")