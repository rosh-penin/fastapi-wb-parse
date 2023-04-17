from fastapi.exceptions import HTTPException
import requests

from models import ObjectModel


def get_response_from_id(nm_id: str):
    """Get response from url by id."""
    response = requests.get(f'https://card.wb.ru/cards/detail?nm={nm_id}')
    if not response or response.status_code == 404:
        raise HTTPException(404, 'There is no such product')
    return response.json()


def lazy_get(nm_id: int, session):
    """DRY getting object."""
    obj = session.get(ObjectModel, nm_id)
    if not obj:
        raise HTTPException(404, "There is no such product in db.")
    return obj
