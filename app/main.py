from os import getenv

from fastapi import Body, FastAPI, Response
from fastapi.exceptions import HTTPException
import requests
from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker

DB_ENGINE = getenv('DB_ENGINE', None)
DB_USER = getenv('POSTGRES_USER', None)
DB_PASS = getenv('POSTGRES_PASSWORD', None)
DB_NAME = getenv('DB_NAME', None)
DB_HOST = getenv('DB_HOST', None)
DB_PORT = getenv('DB_PORT', None)

if DB_ENGINE:
    engine = create_engine(f'{DB_ENGINE}://{DB_USER}:{DB_PASS}@{DB_HOST}:'
                           f'{DB_PORT}/{DB_NAME}')
else:
    engine = create_engine('sqlite:///mydatabase.db', echo=True)

Session = sessionmaker(engine)
api = FastAPI()
Base = declarative_base()


class ColorModel(Base):
    """ORM model for wares colors. Seems useless."""
    __tablename__ = 'colors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    objects: Mapped[list['ObjectModel']] = relationship(
        back_populates='colors'
    )


class ObjectModel(Base):
    """ORM model for wares."""
    __tablename__ = 'things'

    nm_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    brand: Mapped[str]
    brand_id: Mapped[int]
    site_brand_id: Mapped[int]
    supplier_id: Mapped[int]
    sale: Mapped[int]
    price: Mapped[int]
    sale_price: Mapped[int]
    rating: Mapped[float]
    feedbacks: Mapped[int]
    color_id: Mapped[int] = mapped_column(ForeignKey('colors.id'))
    colors: Mapped['ColorModel'] = relationship(back_populates='objects')

    def json(self):
        return {
            'nm_id': self.nm_id,
            'name': self.name,
            'brand': self.brand,
            'brand_id': self.brand_id,
            'site_brand_id': self.site_brand_id,
            'supplier_id': self.supplier_id,
            'sale': self.sale,
            'price': self.price,
            'sale_price': self.sale_price,
            'rating': self.rating,
            'feedbacks': self.feedbacks,
            'colors': {'id': self.colors.id, 'name': self.colors.name}
        }


Base.metadata.create_all(engine)


def get_response_from_id(id: str):
    """Get response from url by id."""
    response = requests.get(f'https://card.wb.ru/cards/detail?nm={id}')
    if not response or response.status_code == 404:
        raise HTTPException(404, 'There is no such product')

    return response.json()


@api.post('/wares/')
def add_product(request: dict = Body(...)):
    """Call parser and creates new db entities in corresponding models."""
    response = get_response_from_id(request.get('nm_id'))
    # Should be possible to try-except next block
    # Too many direct indexing
    product = response['data']['products'][0]
    colors = product['colors'][0]
    with Session.begin() as session:
        if session.get(ObjectModel, product['id']):
            raise HTTPException(400, 'This product already exists in db.')
        db_colors = session.get(ColorModel, colors['id'])
        if db_colors:
            colors = db_colors
        else:
            colors = ColorModel(**colors)
        product_db = ObjectModel(
            nm_id=product['id'],
            name=product['name'],
            brand=product['brand'],
            brand_id=product['brandId'],
            site_brand_id=product['siteBrandId'],
            supplier_id=product['supplierId'],
            sale=product['sale'],
            price=product['priceU'],
            sale_price=product['salePriceU'],
            rating=product['rating'],
            feedbacks=product['feedbacks'],
            colors=colors
        )
        session.add(product_db)

        return product_db.json()


@api.get('/wares/')
def get_products():
    """Returns all objects in ObjectModel model."""
    with Session() as session:

        return [obj.json() for obj in session.scalars(
            select(ObjectModel).join(ObjectModel.colors)
        ).all()]


def lazy_get(nm_id, session):
    """DRY getting object."""
    obj = session.get(ObjectModel, nm_id)
    if not obj:
        raise HTTPException(404, "There is no such product in db.")

    return obj


@api.get('/wares/{nm_id}/')
def get_product(nm_id: int):
    """Return selected product."""
    with Session() as session:
        obj = lazy_get(nm_id, session)

        return obj.json()


@api.delete('/wares/{nm_id}/')
def delete_product(nm_id: int):
    """Delete object from db."""
    with Session.begin() as session:
        obj = lazy_get(nm_id, session)
        session.delete(obj)

        return Response(status_code=204)
