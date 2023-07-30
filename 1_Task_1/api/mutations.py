from datetime import date
from ariadne import convert_kwargs_to_snake_case
from api import db
from api.models import BankCard


@convert_kwargs_to_snake_case
def create_card_resolver(obj, info, card_id, card_number, cvv, card_type, person):
    try:
        today = date.today()
        card = BankCard(
            card_id=card_id, card_number=card_number, end_date=today, cvv=cvv, card_type=card_type, person=person, is_active=True
        )
        db.session.add(card)
        db.session.commit()
        payload = {
            "success": True,
            "card": card.to_dict()
        }
    except ValueError:
        payload = {
            "success": False,
            "errors": [f"Введены некорректные данные"]
        }
    return payload


@convert_kwargs_to_snake_case
def deleteCard_resolver(obj, info, id):
    try:
        card = BankCard.query.get(id)
        if card:
            db.session.delete(card)
            db.session.commit()
            payload = {
                "success": True,
                "message": f"Карта с номером {id} успешно удалена"
            }
        else:
            payload = {
                "success": False,
                "errors": [f"Карта под номером {id} не найдена"]
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def updateCard_resolver(obj, info, id, new_card_data=None):
    try:
        card = BankCard.query.get(id)
        if new_card_data is not None:
            for key, value in new_card_data.items():
                setattr(card, key, value)
            db.session.commit()
            payload = {
                "success": True,
                "card": card.to_dict(),
            }
        elif not card:
            payload = {
                "success": False,
                "errors": [f"Карта с ID {id} не найдена"]
            }
        else:
            payload = {
                "success": False,
                "errors": ["Нет данных для обновления"]
            }
    except Exception as error:
        db.session.rollback()
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
