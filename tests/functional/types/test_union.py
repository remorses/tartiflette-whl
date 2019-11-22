import pytest

from tartiflette import Resolver, create_engine


@pytest.fixture(scope="module")
async def ttftt_engine():
    schema_sdl = """
    type One {
        aField: String
        bField: Int
    }

    type Two {
        cField: Int
        dField: String
    }

    type Three {
        eField: Float
        fField: String
    }

    union Mixed = One | Two | Three

    type Query {
        test(choose: Int!): Mixed
    }
    """

    @Resolver("Query.test", schema_name="test_union")
    async def func_field_resolver(
        parent, arguments, request_ctx, info: "ResolveInfo"
    ):
        chosen = arguments.get("choose", 0)
        if chosen == 1:
            return {"aField": "aValue", "bField": 1, "_typename": "One"}
        elif chosen == 2:

            class Lol:
                def __init__(self, *args, **kwargs):
                    self._typename = "Two"
                    self.cField = 2
                    self.dField = "dValue"

            return Lol()
        elif chosen == 3:

            class Three:
                def __init__(self, *args, **kwargs):
                    self.eField = 3.6
                    self.fField = "fValue"

            return Three()

        return None

    return await create_engine(schema_sdl, schema_name="test_union")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        query aquery {
            test(choose:1){
                ... on One {
                    aField
                    bField
                }
                ... on Two {
                    cField
                    dField
                }
                ... on Three {
                    eField
                    fField
                }
            }
        }
        """,
            {"data": {"test": {"aField": "aValue", "bField": 1}}},
        ),
        (
            """
        query aquery {
            test(choose:2){
                ... on One {
                    aField
                    bField
                }
                ... on Two {
                    cField
                    dField
                }
                ... on Three {
                    eField
                    fField
                }
            }
        }
        """,
            {"data": {"test": {"cField": 2, "dField": "dValue"}}},
        ),
        (
            """
        query aquery {
            test(choose:3){
                ... on One {
                    aField
                    bField
                }
                ... on Two {
                    cField
                    dField
                }
                ... on Three {
                    eField
                    fField
                }
            }
        }
        """,
            {"data": {"test": {"eField": 3.6, "fField": "fValue"}}},
        ),
        (
            """

        fragment bob on One {
            __typename
            aField
            bField
        }

        fragment ninja on Two {
            __typename
            cField
            dField
        }

        fragment lol on Three {
            __typename
            eField
            fField
        }

        query aquery {
            test(choose:3){
                ... bob
                ... ninja
                ... lol
            }
            __typename
        }
        """,
            {
                "data": {
                    "test": {
                        "__typename": "Three",
                        "eField": 3.6,
                        "fField": "fValue",
                    },
                    "__typename": "Query",
                }
            },
        ),
    ],
)
async def test_tartiflette_execute_union_type_output(
    query, expected, ttftt_engine
):
    result = await ttftt_engine.execute(query, operation_name="aquery")

    assert expected == result
