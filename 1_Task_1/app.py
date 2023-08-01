from api import app, db
from ariadne import (load_schema_from_path, make_executable_schema, 
                     graphql_sync, snake_case_fallback_resolvers, ObjectType)
from ariadne.constants import HTTP_STATUS_200_OK
from flask import request, jsonify
from api.queries import listCards_revolver, getCard_resolver
from api.mutations import create_card_resolver, deleteCard_resolver, updateCard_resolver


query = ObjectType("Query")
query.set_field("listCards", listCards_revolver)
query.set_field("getCard", getCard_resolver)


mutation = ObjectType("Mutation")
mutation.set_field("createCard", create_card_resolver)
mutation.set_field("deleteCard", deleteCard_resolver)
mutation.set_field("updateCard", updateCard_resolver)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["GET", "POST"])
def graphql_server():
    if request.method == "GET":
        return HTTP_STATUS_200_OK, 200
    elif request.method == "POST":
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code
