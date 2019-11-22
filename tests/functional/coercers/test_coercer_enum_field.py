import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion", resolvers={"Query.enumField": resolve_unwrapped_field}
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        ("""query { enumField }""", None, {"data": {"enumField": "SUCCESS"}}),
        (
            """query { enumField(param: null) }""",
            None,
            {"data": {"enumField": "SUCCESS-None"}},
        ),
        (
            """query { enumField(param: ENUM_2) }""",
            None,
            {"data": {"enumField": "SUCCESS-ENUM_2_2-MyEnum-enumField"}},
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            None,
            {"data": {"enumField": "SUCCESS"}},
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": None},
            {"data": {"enumField": "SUCCESS-None"}},
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"enumField": "SUCCESS-ENUM_3_3-MyEnum-enumField"}},
        ),
        (
            """query ($param: MyEnum = null) { enumField(param: $param) }""",
            None,
            {"data": {"enumField": "SUCCESS-None"}},
        ),
        (
            """query ($param: MyEnum = null) { enumField(param: $param) }""",
            {"param": None},
            {"data": {"enumField": "SUCCESS-None"}},
        ),
        (
            """query ($param: MyEnum = null) { enumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"enumField": "SUCCESS-ENUM_3_3-MyEnum-enumField"}},
        ),
        (
            """query ($param: MyEnum = ENUM_4) { enumField(param: $param) }""",
            None,
            {"data": {"enumField": "SUCCESS-ENUM_4_4-MyEnum-enumField"}},
        ),
        (
            """query ($param: MyEnum = ENUM_4) { enumField(param: $param) }""",
            {"param": None},
            {"data": {"enumField": "SUCCESS-None"}},
        ),
        (
            """query ($param: MyEnum = ENUM_4) { enumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"enumField": "SUCCESS-ENUM_3_3-MyEnum-enumField"}},
        ),
        (
            """query ($param: MyEnum!) { enumField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { enumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { enumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"enumField": "SUCCESS-ENUM_3_3-MyEnum-enumField"}},
        ),
    ],
)
async def test_coercion_enum_field(engine, query, variables, expected):
    assert await engine.execute(query, variables=variables) == expected
