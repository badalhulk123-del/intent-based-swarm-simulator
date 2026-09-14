import os
import numpy as np
import matplotlib.pyplot as plt

def plot_simulation(sim, outdir):
    os.makedirs(outdir, exist_ok=True)

    plt.figure()
    for aid, points in sim.trajectories.items():
        p = np.array(points)
        plt.plot(p[:, 0], p[:, 1], linewidth=1)
    completed = np.array([t.position for t in sim.tasks if t.completed])
    pending = np.array([t.position for t in sim.tasks if not t.completed])
    if len(completed):
        plt.scatter(completed[:, 0], completed[:, 1], marker="o", label="Completed")
    if len(pending):
        plt.scatter(pending[:, 0], pending[:, 1], marker="x", label="Pending")
    plt.xlim(0, sim.cfg.world_size)
    plt.ylim(0, sim.cfg.world_size)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Swarm survey trajectories")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "trajectories.png"), dpi=150)
    plt.close()

    plt.figure()
    plt.plot([r.step for r in sim.records], [r.coverage for r in sim.records])
    plt.xlabel("Step")
    plt.ylabel("Coverage")
    plt.ylim(0, 1.05)
    plt.title("Coverage over time")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "coverage.png"), dpi=150)
    plt.close()

    plt.figure()
    plt.plot([r.step for r in sim.records], [r.failures for r in sim.records])
    plt.xlabel("Step")
    plt.ylabel("Cumulative failures")
    plt.title("Fault injection")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "faults.png"), dpi=150)
    plt.close()

def plot_monte_carlo(results, outdir):
    os.makedirs(outdir, exist_ok=True)
    coverages = [r["coverage"] for r in results]
    failures = [r["failures"] for r in results]

    plt.figure()
    plt.hist(coverages, bins=min(10, max(1, len(coverages))))
    plt.xlabel("Final coverage")
    plt.ylabel("Runs")
    plt.title("Monte Carlo coverage")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "monte_carlo_coverage.png"), dpi=150)
    plt.close()

    plt.figure()
    plt.hist(failures, bins=min(10, max(1, len(failures))))
    plt.xlabel("Failures")
    plt.ylabel("Runs")
    plt.title("Monte Carlo failures")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "monte_carlo_failures.png"), dpi=150)
    plt.close()
