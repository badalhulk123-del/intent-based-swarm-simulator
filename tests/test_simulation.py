from src.swarm_sim.config import Config
from src.swarm_sim.simulation import Simulator

def test_simulation_runs():
    sim = Simulator(Config(n_agents=4, n_tasks=6, steps=20, seed=1))
    records = sim.run(required_coverage=0.5)
    assert records
    assert 0.0 <= sim.coverage() <= 1.0
    assert len(sim.trajectories) == 4

def test_deterministic_seed():
    cfg = Config(n_agents=4, n_tasks=6, steps=20, seed=42)
    a = Simulator(cfg)
    b = Simulator(cfg)
    a.run()
    b.run()
    assert a.coverage() == b.coverage()
    assert a.failures == b.failures
