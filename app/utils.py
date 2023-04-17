from fastapi.exceptions import HTTPException
import requests

from models import ObjectModel


def get_response_from_id(id: str):
    """Get response from url by id."""
    response = requests.get(f'https://card.wb.ru/cards/detail?nm={id}')
    print('IS LOGGING WORKING?')
    print(response)
    if not response or response.status_code == 404:
        print('PROBLEM ARISES BUT IGNORED.')
        raise HTTPException(404, 'There is no such product')

    return response.json()


def lazy_get(nm_id, session):
    """DRY getting object."""
    obj = session.get(ObjectModel, nm_id)
    if not obj:
        raise HTTPException(404, "There is no such product in db.")

    return obj
