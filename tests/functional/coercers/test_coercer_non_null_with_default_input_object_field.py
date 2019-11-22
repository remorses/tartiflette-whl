import pytest

from tests.functional.coercers.common import resolve_input_object_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={
        "Query.nonNullWithDefaultInputObjectField": resolve_input_object_field
    },
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullWithDefaultInputObjectField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Missing mandatory argument < param > in field < Query.nonNullWithDefaultInputObjectField >.",
                        "path": ["nonNullWithDefaultInputObjectField"],
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "rule": "5.4.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                            "tag": "required-arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullWithDefaultInputObjectField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": ["nonNullWithDefaultInputObjectField"],
                        "locations": [{"line": 1, "column": 44}],
                        "extensions": {
                            "rule": "5.6.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Values-of-Correct-Type",
                            "tag": "values-of-correct-type",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullWithDefaultInputObjectField(param: {}) }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """
            query {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              })
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """
            query {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              })
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """
            query {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: false
                enumField: ENUM_2
                floatField: 23456.789e2
                intField: 10
                stringField: "paramDefaultValue"
                listBooleanField: false
                listEnumField: ENUM_2
                listFloatField: 23456.789e2
                listIntField: 10
                listStringField: "paramDefaultValue"
              })
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_2_2-MyEnum-enumField]-"
                    "[floatField:2345681.9]-"
                    "[intField:13]-"
                    "[stringField:paramdefaultvalue-scalar-stringField]-"
                    "[listBooleanField:False]-"
                    "[listEnumField:enum_2_2-myenum]-"
                    "[listFloatField:2345681.9]-"
                    "[listIntField:13]-"
                    "[listStringField:paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """
            query {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: false
                enumField: ENUM_2
                floatField: 23456.789e2
                intField: 10
                stringField: "paramDefaultValue"
                listBooleanField: [false]
                listEnumField: [ENUM_2]
                listFloatField: [23456.789e2]
                listIntField: [10]
                listStringField: ["paramDefaultValue"]
              })
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_2_2-MyEnum-enumField]-"
                    "[floatField:2345681.9]-"
                    "[intField:13]-"
                    "[stringField:paramdefaultvalue-scalar-stringField]-"
                    "[listBooleanField:False]-"
                    "[listEnumField:enum_2_2-myenum]-"
                    "[listFloatField:2345681.9]-"
                    "[listIntField:13]-"
                    "[listStringField:paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """
            query {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: false
                enumField: ENUM_2
                floatField: 23456.789e2
                intField: 10
                stringField: "paramDefaultValue"
                listBooleanField: [false, null]
                listEnumField: [ENUM_2, null]
                listFloatField: [23456.789e2, null]
                listIntField: [10, null]
                listStringField: ["paramDefaultValue", null]
              })
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_2_2-MyEnum-enumField]-"
                    "[floatField:2345681.9]-"
                    "[intField:13]-"
                    "[stringField:paramdefaultvalue-scalar-stringField]-"
                    "[listBooleanField:False-None]-"
                    "[listEnumField:enum_2_2-myenum-None]-"
                    "[listFloatField:2345681.9-None]-"
                    "[listIntField:13-None]-"
                    "[listStringField:paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < MyInputWithDefault! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {"param": {}},
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault! = null) { nonNullWithDefaultInputObjectField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 38}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInputWithDefault! = null) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInputWithDefault! = null) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {"param": {}},
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault! = null) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault! = null) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault! = null) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault! = null) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault! = null) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": None},
            {
                "data": {"nonNullWithDefaultInputObjectField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": ["nonNullWithDefaultInputObjectField"],
                        "locations": [{"line": 15, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": {}},
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": None},
            {
                "data": {"nonNullWithDefaultInputObjectField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": ["nonNullWithDefaultInputObjectField"],
                        "locations": [{"line": 15, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": {}},
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_4_4-MyEnum-enumField]-"
                    "[floatField:45681.9]-"
                    "[intField:33]-"
                    "[stringField:vardefault-scalar-stringField]-"
                    "[listBooleanField:False]-"
                    "[listEnumField:enum_4_4-myenum]-"
                    "[listFloatField:45681.9]-"
                    "[listIntField:33]-"
                    "[listStringField:vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": None},
            {
                "data": {"nonNullWithDefaultInputObjectField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": ["nonNullWithDefaultInputObjectField"],
                        "locations": [{"line": 15, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": {}},
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_4_4-MyEnum-enumField]-"
                    "[floatField:45681.9]-"
                    "[intField:33]-"
                    "[stringField:vardefault-scalar-stringField]-"
                    "[listBooleanField:False]-"
                    "[listEnumField:enum_4_4-myenum]-"
                    "[listFloatField:45681.9]-"
                    "[listIntField:33]-"
                    "[listStringField:vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": None},
            {
                "data": {"nonNullWithDefaultInputObjectField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": ["nonNullWithDefaultInputObjectField"],
                        "locations": [{"line": 15, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": {}},
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_4_4-MyEnum-enumField]-"
                    "[floatField:45681.9]-"
                    "[intField:33]-"
                    "[stringField:vardefault-scalar-stringField]-"
                    "[listBooleanField:False-None]-"
                    "[listEnumField:enum_4_4-myenum-None]-"
                    "[listFloatField:45681.9-None]-"
                    "[listIntField:33-None]-"
                    "[listStringField:vardefault-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": None},
            {
                "data": {"nonNullWithDefaultInputObjectField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": ["nonNullWithDefaultInputObjectField"],
                        "locations": [{"line": 15, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {"param": {}},
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: MyInputWithDefault = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              nonNullWithDefaultInputObjectField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < MyInputWithDefault! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyInputWithDefault! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {"param": {}},
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: MyInputWithDefault!) { nonNullWithDefaultInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_1_1-myenum-None]-"
                    "[listFloatField:12345681.9-None]-"
                    "[listIntField:123459-None]-"
                    "[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_4_4-MyEnum-enumField]-"
                    "[floatField:45681.9]-"
                    "[intField:33]-"
                    "[stringField:vardefault-scalar-stringField]-"
                    "[listBooleanField:False]-"
                    "[listEnumField:enum_4_4-myenum]-"
                    "[listFloatField:45681.9]-"
                    "[listIntField:33]-"
                    "[listStringField:vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_4_4-MyEnum-enumField]-"
                    "[floatField:45681.9]-"
                    "[intField:33]-"
                    "[stringField:vardefault-scalar-stringField]-"
                    "[listBooleanField:False]-"
                    "[listEnumField:enum_4_4-myenum]-"
                    "[listFloatField:45681.9]-"
                    "[listIntField:33]-"
                    "[listStringField:vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_4_4-MyEnum-enumField]-"
                    "[floatField:45681.9]-"
                    "[intField:33]-"
                    "[stringField:vardefault-scalar-stringField]-"
                    "[listBooleanField:False-None]-"
                    "[listEnumField:enum_4_4-myenum-None]-"
                    "[listFloatField:45681.9-None]-"
                    "[listIntField:33-None]-"
                    "[listStringField:vardefault-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:None]-"
                    "[listEnumField:None]-"
                    "[listFloatField:None]-"
                    "[listIntField:None]-"
                    "[listStringField:None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > of required type < [MyEnum]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > of required type < [Float]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > of required type < [Int]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > of non-null type < [Boolean]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > of non-null type < [MyEnum]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > of non-null type < [Float]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > of non-null type < [Int]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True-None]-"
                    "[listEnumField:enum_3_3-myenum-None]-"
                    "[listFloatField:345681.9-None]-"
                    "[listIntField:23-None]-"
                    "[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > got invalid value < [None] >; Expected non-nullable type < Boolean! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > got invalid value < [None] >; Expected non-nullable type < MyEnum! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > got invalid value < [None] >; Expected non-nullable type < Float! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > got invalid value < [None] >; Expected non-nullable type < Int! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > got invalid value < [None] >; Expected non-nullable type < String! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > got invalid value < [True, None] >; Expected non-nullable type < Boolean! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > got invalid value < ['ENUM_3', None] >; Expected non-nullable type < MyEnum! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > got invalid value < [345678.9, None] >; Expected non-nullable type < Float! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > got invalid value < [20, None] >; Expected non-nullable type < Int! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > got invalid value < ['varValue', None] >; Expected non-nullable type < String! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > of required type < [Boolean!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > of required type < [MyEnum!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > of required type < [Float!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > of required type < [Int!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > of required type < [String!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": None,
                "listEnumField": None,
                "listFloatField": None,
                "listIntField": None,
                "listStringField": None,
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > of non-null type < [Boolean!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > of non-null type < [MyEnum!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > of non-null type < [Float!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > of non-null type < [Int!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > of non-null type < [String!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > got invalid value < [None] >; Expected non-nullable type < Boolean! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > got invalid value < [None] >; Expected non-nullable type < MyEnum! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > got invalid value < [None] >; Expected non-nullable type < Float! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > got invalid value < [None] >; Expected non-nullable type < Int! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > got invalid value < [None] >; Expected non-nullable type < String! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:True]-"
                    "[listEnumField:enum_3_3-myenum]-"
                    "[listFloatField:345681.9]-"
                    "[listIntField:23]-"
                    "[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > got invalid value < [True, None] >; Expected non-nullable type < Boolean! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > got invalid value < ['ENUM_3', None] >; Expected non-nullable type < MyEnum! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > got invalid value < [345678.9, None] >; Expected non-nullable type < Float! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > got invalid value < [20, None] >; Expected non-nullable type < Int! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > got invalid value < ['varValue', None] >; Expected non-nullable type < String! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $itemBooleanField: Boolean
              $itemEnumField: MyEnum
              $itemFloatField: Float
              $itemIntField: Int
              $itemStringField: String
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_1_1-MyEnum-enumField]-"
                    "[floatField:12345681.9]-"
                    "[intField:123459]-"
                    "[stringField:defaultstring-scalar-stringField]-"
                    "[listBooleanField:False-None]-"
                    "[listEnumField:enum_2_2-myenum-None]-"
                    "[listFloatField:2345681.9-None]-"
                    "[listIntField:13-None]-"
                    "[listStringField:paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $itemBooleanField: Boolean
              $itemEnumField: MyEnum
              $itemFloatField: Float
              $itemIntField: Int
              $itemStringField: String
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "itemBooleanField": None,
                "itemEnumField": None,
                "itemFloatField": None,
                "itemIntField": None,
                "itemStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:False-None]-"
                    "[listEnumField:enum_2_2-myenum-None]-"
                    "[listFloatField:2345681.9-None]-"
                    "[listIntField:13-None]-"
                    "[listStringField:paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $itemBooleanField: Boolean
              $itemEnumField: MyEnum
              $itemFloatField: Float
              $itemIntField: Int
              $itemStringField: String
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "itemBooleanField": True,
                "itemEnumField": "ENUM_3",
                "itemFloatField": 3456.789e2,
                "itemIntField": 20,
                "itemStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:False-True]-"
                    "[listEnumField:enum_2_2-myenum-enum_3_3-myenum]-"
                    "[listFloatField:2345681.9-345681.9]-"
                    "[listIntField:13-23]-"
                    "[listStringField:paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $itemBooleanField: Boolean = null
              $itemEnumField: MyEnum = null
              $itemFloatField: Float = null
              $itemIntField: Int = null
              $itemStringField: String = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:False-None]-"
                    "[listEnumField:enum_2_2-myenum-None]-"
                    "[listFloatField:2345681.9-None]-"
                    "[listIntField:13-None]-"
                    "[listStringField:paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $itemBooleanField: Boolean = null
              $itemEnumField: MyEnum = null
              $itemFloatField: Float = null
              $itemIntField: Int = null
              $itemStringField: String = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "itemBooleanField": None,
                "itemEnumField": None,
                "itemFloatField": None,
                "itemIntField": None,
                "itemStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:False-None]-"
                    "[listEnumField:enum_2_2-myenum-None]-"
                    "[listFloatField:2345681.9-None]-"
                    "[listIntField:13-None]-"
                    "[listStringField:paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $itemBooleanField: Boolean = null
              $itemEnumField: MyEnum = null
              $itemFloatField: Float = null
              $itemIntField: Int = null
              $itemStringField: String = null
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "itemBooleanField": True,
                "itemEnumField": "ENUM_3",
                "itemFloatField": 3456.789e2,
                "itemIntField": 20,
                "itemStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:False-True]-"
                    "[listEnumField:enum_2_2-myenum-enum_3_3-myenum]-"
                    "[listFloatField:2345681.9-345681.9]-"
                    "[listIntField:13-23]-"
                    "[listStringField:paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $itemBooleanField: Boolean = false
              $itemEnumField: MyEnum = ENUM_4
              $itemFloatField: Float = 456.789e2
              $itemIntField: Int = 30
              $itemStringField: String = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            None,
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:False]-"
                    "[enumField:ENUM_4_4-MyEnum-enumField]-"
                    "[floatField:45681.9]-"
                    "[intField:33]-"
                    "[stringField:vardefault-scalar-stringField]-"
                    "[listBooleanField:False-False]-"
                    "[listEnumField:enum_2_2-myenum-enum_4_4-myenum]-"
                    "[listFloatField:2345681.9-45681.9]-"
                    "[listIntField:13-33]-"
                    "[listStringField:paramdefaultvalue-scalar-vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $itemBooleanField: Boolean = false
              $itemEnumField: MyEnum = ENUM_4
              $itemFloatField: Float = 456.789e2
              $itemIntField: Int = 30
              $itemStringField: String = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "itemBooleanField": None,
                "itemEnumField": None,
                "itemFloatField": None,
                "itemIntField": None,
                "itemStringField": None,
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:None]-"
                    "[enumField:None]-"
                    "[floatField:None]-"
                    "[intField:None]-"
                    "[stringField:None]-"
                    "[listBooleanField:False-None]-"
                    "[listEnumField:enum_2_2-myenum-None]-"
                    "[listFloatField:2345681.9-None]-"
                    "[listIntField:13-None]-"
                    "[listStringField:paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $itemBooleanField: Boolean = false
              $itemEnumField: MyEnum = ENUM_4
              $itemFloatField: Float = 456.789e2
              $itemIntField: Int = 30
              $itemStringField: String = "varDefault"
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "itemBooleanField": True,
                "itemEnumField": "ENUM_3",
                "itemFloatField": 3456.789e2,
                "itemIntField": 20,
                "itemStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:False-True]-"
                    "[listEnumField:enum_2_2-myenum-enum_3_3-myenum]-"
                    "[listFloatField:2345681.9-345681.9]-"
                    "[listIntField:13-23]-"
                    "[listStringField:paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $itemBooleanField: Boolean!
              $itemEnumField: MyEnum!
              $itemFloatField: Float!
              $itemIntField: Int!
              $itemStringField: String!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemBooleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemEnumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemFloatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemIntField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemStringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $itemBooleanField: Boolean!
              $itemEnumField: MyEnum!
              $itemFloatField: Float!
              $itemIntField: Int!
              $itemStringField: String!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "itemBooleanField": None,
                "itemEnumField": None,
                "itemFloatField": None,
                "itemIntField": None,
                "itemStringField": None,
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemBooleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemEnumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemFloatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemIntField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemStringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $itemBooleanField: Boolean!
              $itemEnumField: MyEnum!
              $itemFloatField: Float!
              $itemIntField: Int!
              $itemStringField: String!
            ) {
              nonNullWithDefaultInputObjectField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "itemBooleanField": True,
                "itemEnumField": "ENUM_3",
                "itemFloatField": 3456.789e2,
                "itemIntField": 20,
                "itemStringField": "varValue",
            },
            {
                "data": {
                    "nonNullWithDefaultInputObjectField": "SUCCESS-"
                    "[booleanField:True]-"
                    "[enumField:ENUM_3_3-MyEnum-enumField]-"
                    "[floatField:345681.9]-"
                    "[intField:23]-"
                    "[stringField:varvalue-scalar-stringField]-"
                    "[listBooleanField:False-True]-"
                    "[listEnumField:enum_2_2-myenum-enum_3_3-myenum]-"
                    "[listFloatField:2345681.9-345681.9]-"
                    "[listIntField:13-23]-"
                    "[listStringField:paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
    ],
)
async def test_coercer_non_null_with_default_input_object_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
