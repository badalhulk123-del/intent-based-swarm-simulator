import numpy as np

def allocate_tasks(agents, tasks):
    for agent in agents:
        agent.assigned_task = None
    for task in tasks:
        if not task.completed:
            task.assigned_to = None

    alive = [a for a in agents if a.alive]
    pending = [t for t in tasks if not t.completed]
    pairs = []

    for a in alive:
        for t in pending:
            cost = float(np.linalg.norm(a.position - t.position))
            cost += 2.0 * a.completed_tasks
            pairs.append((cost, a.id, t.id))

    pairs.sort()
    used_agents, used_tasks = set(), set()

    for _, aid, tid in pairs:
        if aid in used_agents or tid in used_tasks:
            continue
        agent = next(a for a in alive if a.id == aid)
        task = next(t for t in pending if t.id == tid)
        agent.assigned_task = tid
        task.assigned_to = aid
        used_agents.add(aid)
        used_tasks.add(tid)
