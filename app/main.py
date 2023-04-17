from fastapi import Body, Response
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from engine import api, Session
from models import ObjectModel, ColorModel
from utils import get_response_from_id, lazy_get


@api.post('/wares/')
def add_product(request: dict = Body(...)):
    """Call parser and creates new db entities in corresponding models."""
    response = get_response_from_id(request.get('nm_id'))
    try:
        product = response['data']['products'][0]
    except IndexError:
        raise HTTPException(404, 'There is no such product on wb.')
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
