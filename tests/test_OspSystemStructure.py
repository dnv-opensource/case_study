from pathlib import Path

from libcosimpy.CosimEnums import CosimVariableCausality, CosimVariableType, CosimVariableVariability
from libcosimpy.CosimExecution import CosimExecution  # type: ignore


def test_system_structure():
    path = Path(Path(__file__).parent, "data", "BouncingBall", "OspSystemStructure.xml")
    assert path.exists(), "OspSystemStructure.xml not found"
    sim = CosimExecution.from_osp_config_file(str(path))
    assert sim.execution_status.current_time == 0
    assert sim.execution_status.state == 0
    assert len(sim.slave_infos()) == 1
    assert sim.slave_infos()[0].name.decode() == "bb"
    assert sim.slave_infos()[0].index == 0
    variables = sim.slave_variables(0)
    assert variables[0].name.decode() == "time"
    assert variables[0].reference == 0
    assert variables[0].type == CosimVariableType.REAL.value
    assert variables[0].causality == CosimVariableCausality.LOCAL.value
    assert variables[0].variability == CosimVariableVariability.CONTINUOUS.value
    for v in variables:
        print(v)


if __name__ == "__main__":
    test_system_structure()
