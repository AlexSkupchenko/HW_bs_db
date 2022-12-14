import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker, query

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres:postgres@localhost:5432/bookstore_db'
engine = sqlalchemy.create_engine(DSN)
# create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# with open('fixtures/tests_data.json', 'r') as fd:
#     data = json.load(fd)
#
# for record in data:
#     model = {
#         'publisher': Publisher,
#         'shop': Shop,
#         'book': Book,
#         'stock': Stock,
#         'sale': Sale,
#     }[record.get('model')]
#     session.add(model(id=record.get('pk'), **record.get('fields')))
#
# session.commit()

session.close()

q = session.query(Publisher)
for s in q.all():
    print(s.id, s.name)

with Session() as session:
    query = session.query(Sale, Stock, Book, Shop)
    query = query.join(Stock, Stock.id == Sale.id_stock)
    query = query.join(Book, Book.id == Stock.id_book)\
        .filter(Book.id_publisher == input("Enter the identifier (id) of the publisher: "))
    query = query.join(Shop, Shop.id == Stock.id_shop)

    records = query.all()
    for sale, stock, book, shop in records:
        print(f"{book.title} | {shop.name} | {sale.price} | {sale.date_sale}")
