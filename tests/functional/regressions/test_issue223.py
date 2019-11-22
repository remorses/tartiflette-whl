import json

from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, Scalar, create_engine

_SDL = """

directive @lower on ENUM_VALUE
directive @upper on ENUM_VALUE
directive @capitalized on SCALAR
directive @mapToValue on ENUM
directive @addValue(value: Int = 1) on OBJECT | INPUT_OBJECT

scalar Bobby @capitalized

enum Size {
    XL
    L
    m
    M @lower
    S
    XS
}

enum Color @mapToValue {
    RED
    GREEN @lower @upper
    black
    BLACK @lower
    yellow
    YELLOW @lower @upper @lower
    BROWN
}

input ThisIsAnInputObject @addValue(value: 17) {
    aColor: Color
    value: Int
}

type TShirt {
    size: Size
    color: Color
}

type OKLM @addValue(value: 53) {
    value: Int
}

type Wahou {
    weight: OKLM
    height: OKLM
}

type Query {
    wardrobe: [TShirt]
    bobby: Bobby
    test3(argument1: Color): String
    test4: Color
    test5: Wahou
    test6(argument1: ThisIsAnInputObject): String
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.test5", schema_name="issue223")
    async def resolver_test5(_pr, _args, _ctx, _info):
        return {"weight": {"value": 2}, "height": {"value": 6}}

    @Directive("addValue", schema_name="issue223")
    class AddValue:
        @staticmethod
        async def on_post_input_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node,
            value: Any,
            ctx: Optional[Any],
        ):
            value["value"] = value["value"] + directive_args["value"]
            return await next_directive(parent_node, value, ctx)

        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            value["value"] = value["value"] + directive_args["value"]
            return await next_directive(value, ctx, info)

    @Directive("mapToValue", schema_name="issue223")
    class MapToValue:
        my_map = {"RED": "BROWN", "BROWN": "RED"}

        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            value = MapToValue.my_map.get(value, value)
            return await next_directive(value, ctx, info)

        @staticmethod
        async def on_post_input_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node,
            value: Any,
            ctx: Optional[Any],
        ):
            value = MapToValue.my_map.get(value, value)
            return await next_directive(parent_node, value, ctx)

    @Resolver("Query.test4", schema_name="issue223")
    async def resolver_test4(_pr, _args, _ctx, _info):
        return "BROWN"

    @Resolver("Query.test3", schema_name="issue223")
    @Resolver("Query.test6", schema_name="issue223")
    async def resolver_test3(_pr, args, _ctx, _info):
        return json.dumps(args)

    @Scalar("Bobby", schema_name="issue223")
    class BobbyScalar:
        @staticmethod
        def coerce_output(val):
            return str(val)

        @staticmethod
        def coerce_input(val):
            return str(val)

        @staticmethod
        def parse_literal(ast):
            return ast.value

    @Directive("capitalized", schema_name="issue223")
    class Capitalized:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return await next_directive(value.capitalize(), ctx, info)

    @Directive("lower", schema_name="issue223")
    class Lower:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return await next_directive(value.lower(), ctx, info)

    @Directive("upper", schema_name="issue223")
    class Upper:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return await next_directive(value.upper(), ctx, info)

    @Resolver("Query.wardrobe", schema_name="issue223")
    async def wardrobe_resolver(_pr, _args, _ctx, _info):
        return [
            {"size": "XL", "color": "GREEN"},
            {"size": "M", "color": "BLACK"},
            {"size": "M", "color": "YELLOW"},
        ]

    @Resolver("Query.bobby", schema_name="issue223")
    async def bobby_resolver(_pr, _args, _ctx, _info):
        return "lol"

    return await create_engine(sdl=_SDL, schema_name="issue223")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            "query { wardrobe { size color }}",
            {
                "data": {
                    "wardrobe": [
                        {"size": "XL", "color": "GREEN"},
                        {"size": "m", "color": "black"},
                        {"size": "m", "color": "yellow"},
                    ]
                }
            },
        ),
        ("query { bobby }", {"data": {"bobby": "Lol"}}),
        (
            "query { test3(argument1: RED) }",
            {"data": {"test3": '{"argument1": "BROWN"}'}},
        ),
        ("query { test4 }", {"data": {"test4": "RED"}}),
        (
            "query { test5 { weight { value } height { value } } }",
            {
                "data": {
                    "test5": {"weight": {"value": 55}, "height": {"value": 59}}
                }
            },
        ),
        (
            "query { test6(argument1: { value: 3, aColor: RED })}",
            {
                "data": {
                    "test6": '{"argument1": {"aColor": "BROWN", "value": 20}}'
                }
            },
        ),
    ],
)
async def test_issue223(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected
