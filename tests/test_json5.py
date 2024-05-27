from pathlib import Path

import pytest
from case_study.json5 import Json5Reader, json5_write


def test_json5_syntax():
    assert Json5Reader("Hello World", False).js5 == "{ Hello World }", "Automatic addition of '{}' did not work"

    js = Json5Reader("Hello\nWorld\rHei\n\rHo\r\nHi", auto=False)
    assert js.js5 == "{ Hello World Hei  Ho  Hi }", "Automatic replacement of newlines did not work"
    assert js.line(-1) == "}", "Ending '}' expected"
    assert js.line(3) == "Hei", "Quote of line 3 wrong"
    assert js.line(5) == "Hi", "Quote of line 5 wrong"
    js = Json5Reader("Hello 'W\norld'", 0).js5
    assert Json5Reader("Hello 'W\norld'", 0).js5[10] == "\n", "newline within quotations should not be replaced"
    assert Json5Reader("He'llo 'Wo'rld'", 0).js5 == "{ He'llo 'Wo'rld' }", "Handling of single quotes not correct"
    assert (
        len(Json5Reader("Hello World //added a EOL comment", 0).js5) == len("Hello World //added a EOL comment") + 4
    ), "Length of string not conserved when replacing comment"

    assert Json5Reader("Hello//EOL comment", 0).js5 == "{ Hello              }", "Comment not properly replaced"
    assert Json5Reader("Hello#EOL comment", 0).js5 == "{ Hello             }", "Comment not properly replaced"
    js = Json5Reader("Hello /*Line1\nLine2\n..*/..", 0)
    assert js.js5 == "{ Hello                   .. }", "Incorrect multi-line comment"
    assert Json5Reader("{'Hi':1, Ho:2}").js_py == {"Hi": 1.0, "Ho": 2.0}, "Simple dict expected. Second key without '"
    assert Json5Reader("{'Hello:@#%&/=?World':1}").to_py() == {
        "Hello:@#%&/=?World": 1
    }, "Literal string keys should handle any character, including':' and comments"

    js = Json5Reader("{Start: {\n   'H':1,\n   99:{'e':11,'l':12}},\nLast:999}")
    assert js.to_py() == {"Start": {"H": 1, "99": {"e": 11, "l": 12}}, "Last": 999}, "Dict of dict dict expected"

    assert Json5Reader("{'H':1, 99:['e','l','l','o']}").js_py == {
        "H": 1,
        "99": ["e", "l", "l", "o"],
    }, "List as value expected"

    js = Json5Reader("{'H':1, 99:['e','l','l','o'], 'W':999}")
    assert list(js.js_py.keys()) == ["H", "99", "W"], "Additional or missing main object elements"
    with pytest.raises(AssertionError) as err:
        Json5Reader("{ H : 1,2}")
    assert str(err.value).startswith("Json5 read error at 1(10): No proper key:value:")
    js = Json5Reader(
        "{   spec: {\n     stopTime : '3',\n      bb.h : '10.0',\n      bb.v : '[0.0, 1.0, 3.0]',\n      bb.e : '0.7',\n   }}"
    )
    #        print(js.js5)


def test_json5_write():
    js1 = {"key1": 1.0, "key2": "a string", "key3": ["a", "list", "including", "numbers", 9.9, 1]}
    expected = "{key1:1.0,key2:'a string',key3:['a','list','including','numbers',9.9,1]}"
    assert json5_write(js1, pretty_print=False) == expected, "Simple JSON5 dict"

    js2 = {
        "key1": 1.0,
        "key2": "a string",
        "key3": [
            "a",
            "list",
            "including",
            "numbers",
            9.9,
            1,
            "+ object",
            {"hello": 1, "World": 2, "dict": {"hi": 2.1, "ho": 2.2}},
        ],
    }
    expected = "{key1:1.0,key2:'a string',key3:['a','list','including','numbers',9.9,1,'+ object',{hello:1,World:2,dict:{hi:2.1,ho:2.2}}]}"
    assert json5_write(js2, pretty_print=False) == expected, "Json5 with object within list"

    txt = json5_write(js2, pretty_print=True)
    assert len(txt) == 189, "Length of pretty-printed JSON5"
    print(txt)


def test_read_cases():
    bb_cases = Path(__file__).parent.joinpath("data/BouncingBall0/BouncingBall.cases")
    js = Json5Reader(bb_cases)
    assert js.js_py["name"] == "BouncingBall"


#     def test_case(self):
#         cases = Cases("BouncingBall.cases")
#         print(cases.info())
#         assert cases.get_scalarvariables(cases.system.instances["bb"] == "h")[0].get("name"), "h"
#         )  # single scalar variable
#         vars_der = cases.get_scalarvariables(cases.system.instances["bb"], "der")
#         self.assertTrue(
#             len(vars_der) == 2 and vars_der[1].get("name") == "der(v)"
#         )  # example of a 'vector' of both derivatives

if __name__ == "__main__":
    retcode = pytest.main(
        [
            "-rA",
            "-v",
            __file__,
        ]
    )
    assert retcode == 0, f"Non-zero return code {retcode}"