from ariadne import convert_kwargs_to_snake_case, snake_case_fallback_resolvers


def listCards_revolver(obj, info):
    from .models import BankCard
    try:
        cards = [card.to_dict() for card in BankCard.query.all()]
        print(cards)
        payload = {
            "success": True,
            "cards": cards
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def getCard_resolver(obj, info, id):
    from .models import BankCard
    try:
        card = BankCard.query.get(id)
        payload = {
            "success": True,
            "card": card.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Карта под номером {id} не найдена"]
        }
    return payload