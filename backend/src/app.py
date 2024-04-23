import fastapi
import uvicorn

import src.utils as utils
from src.strawberry.schema import schema as strawberry_schema
from strawberry.asgi import GraphQL

utils.start_sentry()

graphql_app = GraphQL(strawberry_schema)

app = fastapi.FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


if __name__ == "__main__":
    uvicorn.run(app)
