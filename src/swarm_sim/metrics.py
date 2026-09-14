import numpy as np

def summarize(sim):
    total_distance = 0.0
    for points in sim.trajectories.values():
        if len(points) > 1:
            total_distance += float(np.sum(np.linalg.norm(np.diff(np.array(points), axis=0), axis=1)))

    final = sim.records[-1] if sim.records else None
    return {
        "steps": len(sim.records),
        "coverage": sim.coverage(),
        "completed_tasks": sum(t.completed for t in sim.tasks),
        "total_tasks": len(sim.tasks),
        "alive_agents": sum(a.alive for a in sim.agents),
        "failures": sim.failures,
        "communication_events": sim.communication_events,
        "final_average_speed": final.avg_speed if final else 0.0,
        "total_distance": total_distance,
    }

def monte_carlo(make_sim, runs):
    results = []
    for i in range(runs):
        sim = make_sim(i)
        sim.run()
        results.append(summarize(sim))
    return results

def aggregate(results):
    if not results:
        return {}
    keys = ["coverage", "failures", "steps", "total_distance"]
    return {
        key: {
            "mean": float(np.mean([r[key] for r in results])),
            "std": float(np.std([r[key] for r in results])),
            "min": float(np.min([r[key] for r in results])),
            "max": float(np.max([r[key] for r in results])),
        }
        for key in keys
    }
