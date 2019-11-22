import os
from tartiflette import Resolver, Engine
from tartiflette_asgi import TartifletteApp, GraphiQL
from tartiflette_plugin_apollo_federation import ApolloFederationPlugin
from .support import read


DISABLE_GRAPHIQL = bool(os.getenv("DISABLE_GRAPHIQL", False))
GRAPHIQL_DEFAULT_JWT = os.getenv("GRAPHIQL_DEFAULT_JWT", "")
GRAPHIQL_QUERY = os.getenv("GRAPHIQL_DEFAULT_QUERY", "") or read(
    os.getenv("GRAPHIQL_DEFAULT_QUERY_FILE_PATH", "")
)


graphiql = GraphiQL(
    path="/",
    default_headers={"Authorization": "Bearer " + GRAPHIQL_DEFAULT_JWT}
    if GRAPHIQL_DEFAULT_JWT
    else {},
    default_query=GRAPHIQL_QUERY,
)


@Resolver("Query.hello")
async def hello(parent, args, context, info):
    name = args["name"]
    return f"Hello, {name}!"


sdl = """
type Query { 
    hello(name: String): String
}
"""

engine = Engine(sdl=sdl, modules=[ApolloFederationPlugin(engine_sdl=sdl)])
app = TartifletteApp(
    engine=engine, path="/", graphiql=graphiql if not DISABLE_GRAPHIQL else False
)

