from pathlib import Path

from case_study.case import Cases


def test_run_casex():
    path = Path(Path(__file__).parent, "data/SimpleTable/test.cases")
    assert path.exists(), "SimpleTable cases file not found"
    cases = Cases(path)
    _ = cases.case_by_name("base")
    _ = cases.case_by_name("case1")
    _ = cases.case_by_name("caseX")
    print("RESULTS", cases.run_case("caseX", "results"))
