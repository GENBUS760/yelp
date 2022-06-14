from peewee import OperationalError
from models import Business
from models import Review
from models import User
from models import Checkin
from models import Category
from models import Friend
from models import Tip
import json
import decimal
from datetime import datetime

import sys

def iterate_file(model_name, shortcircuit=True, status_frequency=500):
    i = 0
    jsonfilename = "yelp_academic_dataset_%s.json" % model_name.lower()
    with open(jsonfilename) as jfile:
        for line in jfile:
            i += 1
            yield json.loads(line)
            if i % status_frequency == 0:
                print("Status >>> %s: %d" % (jsonfilename, i))
                if shortcircuit and i == 10:
                    raise StopIteration()
                    
    
def save_businesses():
    for bdata in iterate_file("business", shortcircuit=False):
        business = Business()
        business.business_id = bdata['business_id']
        business.name = bdata['name']
        business.address = bdata['address']
        business.postal_code = bdata['postal_code']
        business.city = bdata['city']
        business.state = bdata['state']
        business.latitude = bdata['latitude']
        business.longitude = bdata['longitude']
        business.stars = decimal.Decimal(bdata.get('stars', 0))
        business.review_count = int(bdata['review_count'])
        business.is_open = True if bdata['is_open'] == "True" else False
        business.save()

        save_categories(bdata['business_id'], bdata['categories'])


def save_categories(business_id, cat_jarray):
    if cat_jarray is None:
        return
    for name in cat_jarray:
        category = Category()
        category.business_id = business_id
        category.category_name = name
        category.save()


def save_reviews():
    for rdata in iterate_file("review", shortcircuit=False):
        rev = Review()
        rev.review_id = rdata['review_id']
        rev.business_id = rdata['business_id']
        rev.user_id = rdata['user_id']
        rev.stars = int(rdata.get('stars', 0))
        rev.text = rdata['text']
        rev.date = datetime.strptime(rdata['date'].split(" ")[0], "%Y-%m-%d")
        rev.useful_votes = int(rdata['useful'])
        rev.funny_votes = int(rdata['funny'])
        rev.cool_votes = int(rdata['cool'])
        rev.save()


def save_users():
    for udata in iterate_file("user", shortcircuit=False):
        user = User()
        user.user_id = udata['user_id']
        user.name = udata['name']
        user.review_count = int(udata['review_count'])
        user.yelping_since = datetime.strptime(udata['yelping_since'].split(" ")[0], "%Y-%m-%d")
        user.average_stars = decimal.Decimal(udata.get('average_stars', 0))
        
        user.useful_votes = int(udata['useful'])
        user.funny_votes = int(udata['funny'])
        user.cool_votes = int(udata['cool'])
        user.fans = int(udata['fans'])
        
        user.compliment_hot = int(udata['compliment_hot'])
        user.compliment_more = int(udata['compliment_more'])
        user.compliment_profile = int(udata['compliment_profile'])
        user.compliment_cute = int(udata['compliment_cute'])
        user.compliment_list = int(udata['compliment_list'])
        user.compliment_note = int(udata['compliment_note'])
        user.compliment_plain = int(udata['compliment_plain'])
        user.compliment_cool = int(udata['compliment_cool'])
        user.compliment_funny = int(udata['compliment_funny'])
        user.compliment_writer = int(udata['compliment_writer'])
        user.compliment_photos = int(udata['compliment_photos'])
        
        user.save()
        
        save_friends(udata['user_id'], udata['friends'].split(", "))


def save_friends(user_id, cat_jarray):
    if cat_jarray is None:
        return
    for friend_id in cat_jarray:
        friend = Friend()
        friend.user_id = user_id
        friend.friend_id = friend_id
        friend.save()


def save_checkins():
    for cdata in iterate_file("checkin", shortcircuit=False):
        checkin = Checkin()
        checkin.business_id = cdata['business_id']
        for day in range(7):
            for hour in range(24):
                number = int(cdata['checkin_info'].get("%s-%s" % (hour, day), 0))
                if day is 0:
                    checkin.sunday_count += number
                elif day is 1:
                    checkin.monday_count += number
                elif day is 2:
                    checkin.tuesday_count += number
                elif day is 3:
                    checkin.wednesday_count += number
                elif day is 4:
                    checkin.thursday_count += number
                elif day is 5:
                    checkin.friday_count += number
                elif day is 6:
                    checkin.saturday_count += number
                    checkin.save()


def save_tips():
    for tdata in iterate_file("tip", shortcircuit=True):
        tip = Tip()
        tip.business_id = tdata['business_id']
        tip.text = tdata['text']
        tip.user_id = tdata['user_id']
        tip.date = datetime.strptime(tdata['date'], "%Y-%m-%d")
        tip.likes = int(tdata['likes'])
        tip.save()


def reset_database():
    tables = (Business, Review, User, Category, Friend)
    for table in tables:
        # Nuke the Tables
        try:
            table.drop_table()
        except OperationalError:
            pass
        # Create the Tables
        try:
            table.create_table()
        except OperationalError:
            pass
    

if __name__ == "__main__":

    table = sys.argv[1]
    assert table is not None
    assert table in ["reset", "business", "user", "review"]

    if table == "reset":
        reset_database()
    elif table == "business":
        save_businesses()
    elif table == "user":
        save_users()
    elif table == "review":
        save_reviews()
    
    #save_checkins()
    #save_tips()
