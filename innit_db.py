from ext import db
from app import app
from models import User, Comments, Product
from app import app  # შემოგვაქვს შენი მთავარი აპლიკაცია
from ext import db   # 🎯 შემოგვაქვს უკვე არსებული db ობიექტი (თუ app.py-ში გაქვს, შეცვალე: from app import db)
from models import User, Product  # შემოგვაქვს მოდელები, რომ ბაზამ მათი სტრუქტურა დაინახოს

# ფლასკის კონტექსტში ვქმნით ცხრილებს
with app.app_context():
    print("მონაცემთა ბაზის ცხრილები იქმნება...")
    db.create_all()  # ეს ბრძანება შექმნის ყველა ცხრილს (ახალ gender სვეტთან ერთად!)
    print("ბაზა წარმატებით განახლდა და შეიქმნა! 🚀")