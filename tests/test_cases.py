from pathlib import Path

from case_study.case import Cases
from case_study.simulator_interface import SimulatorInterface


def _file(file: str = "BouncingBall.cases"):
    path = Path(__file__).parent.joinpath(file)
    assert path.exists(), f"File {file} does not exist at {Path(__file__).parent}"
    return path


# def test_tuple_iter():
#     """Test of the features provided by the Case class"""
#
#     def check(gen: Generator, expectation: list):
#         lst = [x[0] for x in gen]
#         assert lst == expectation, f"Expected: {expectation}. Found: {lst}"
#
#     tpl20 = tuple(range(20))
#     check(tuple2_iter(tpl20, tpl20, "3"), [3])
#     check(tuple2_iter(tpl20, tpl20, "3:7"), [3, 4, 5, 6, 7])
#     check(tuple2_iter(tpl20, tpl20, ":3"), list(range(0, 4)))
#     check(tuple2_iter(tpl20, tpl20, "17:"), list(range(17, 20)))
#     check(tuple2_iter(tpl20, tpl20, "10:-5"), list(range(10, 16)))
#     check(tuple2_iter(tpl20, tpl20, ":"), list(range(20)))
#     check(tuple2_iter(tpl20, tpl20, "1,3,4,9"), [1, 3, 4, 9])


def test_cases_management():
    cases = Cases(Path.cwd().parent / "data" / "SimpleTable" / "test.cases")
    assert cases.results.results == {}
    assert cases.case_var_by_ref(0, 1) == (
        "x",
        (1,),
    ), f"Case variable of model 0, ref 1: {cases.case_var_by_ref( 0, 1)}"
    assert cases.case_var_by_ref("tab", 1) == ("x", (1,)), "Same with model by name"


def test_cases():
    """Test of the features provided by the Cases class"""
    sim = SimulatorInterface(_file("data/BouncingBall0/OspSystemStructure.xml"))
    cases = Cases(_file("data/Bouncingball0/BouncingBall.cases"), sim)

    print(cases.info())
    # cases.spec
    assert cases.spec["name"] == "BouncingBall", "BouncingBall expected as cases name"
    msg = f"Description: {cases.spec['description']}"
    descr = cases.spec["description"]
    assert isinstance(descr, str) and descr.startswith("Simple Case Study with the"), msg
    assert cases.spec.get("modelFile", "") == "OspSystemStructure.xml", "modelFile not as expected"
    for c in ("base", "restitution", "restitutionAndGravity", "gravity"):
        assert c in cases.spec, f"The case '{c}' is expected to be defined in {cases.spec['name']}"
    # find_by_name
    for c in cases.base.list_cases(as_name=False, flat=True):
        assert cases.case_by_name(c.name).name == c.name, f"Case {c.name} not found in hierarchy"
    assert cases.case_by_name("case99") is None, "Case99 was not expected to be found"
    c_gravity = cases.case_by_name("gravity")
    assert c_gravity is not None and c_gravity.name == "gravity", "'gravity' is expected to exist"
    msg = "'restitution' should not exist within the sub-hierarchy of 'gravity'"
    assert c_gravity is not None and c_gravity.case_by_name("restitution") is None, msg
    c_r = cases.case_by_name("restitution")
    msg = "'restitutionAndGravity' should exist within the sub-hierarchy of 'restitution'"
    assert c_r is not None and c_r.case_by_name("restitutionAndGravity") is not None, msg
    gravity_case = cases.case_by_name("gravity")
    assert gravity_case is not None and gravity_case.name == "gravity", "'gravity' is expected to exist"
    msg = "'case2' should not exist within the sub-hierarchy of 'gravity'"
    assert gravity_case is not None and gravity_case.case_by_name("case2") is None, msg
    restitution_case = cases.case_by_name("restitution")
    msg = "'restitutionAndGravity' should exist within the sub-hierarchy of 'restitution_case'"
    assert restitution_case is not None and restitution_case.case_by_name("restitutionAndGravity") is not None, msg
    # variables (aliases)
    assert cases.variables["h"]["model"] == 0
    assert cases.variables["h"]["instances"] == ("bb",)
    assert cases.variables["h"]["variables"] == (1,)
    assert cases.variables["h"]["description"] == "Position (z) of the ball"
    assert cases.variables["h"]["type"] == 0
    assert cases.variables["h"]["causality"] == 2
    assert cases.variables["h"]["variability"] == 4
    vs = dict((k, v) for k, v in cases.variables.items() if k.startswith("v"))
    assert all(x in vs for x in ("v_min", "v_z", "v"))
