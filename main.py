import argparse
import json
import os

from src.swarm_sim.config import Config
from src.swarm_sim.metrics import aggregate, monte_carlo, summarize
from src.swarm_sim.simulation import Simulator
from src.swarm_sim.visualization import plot_monte_carlo, plot_simulation

def build_config(args, seed=None):
    return Config(
        n_agents=args.agents,
        n_tasks=args.tasks,
        steps=args.steps,
        seed=args.seed if seed is None else seed,
    )

def main():
    parser = argparse.ArgumentParser(description="Safe swarm survey/coverage simulator")
    parser.add_argument("--agents", type=int, default=10)
    parser.add_argument("--tasks", type=int, default=18)
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    os.makedirs("outputs", exist_ok=True)

    if args.runs == 1:
        sim = Simulator(build_config(args))
        sim.run()
        summary = summarize(sim)
        plot_simulation(sim, "outputs")
        with open("outputs/summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(json.dumps(summary, indent=2))
    else:
        def factory(i):
            return Simulator(build_config(args, seed=args.seed + i))

        results = monte_carlo(factory, args.runs)
        summary = aggregate(results)
        plot_monte_carlo(results, "outputs")
        with open("outputs/monte_carlo_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
