from env.environment import CivicEnv


def grade_task(task):
    env = CivicEnv()

    # Load given state
    env.current_state = task["state"]

    # Simple baseline action (we improve later)
    action = {
        "department": "road",
        "priority": "high",
        "resources": 1
    }

    _, reward, _, _ = env.step(action)

    return reward


def run_all_tasks():
    from env.tasks import easy_task, medium_task, hard_task

    tasks = [easy_task(), medium_task(), hard_task()]

    results = {}

    for task in tasks:
        score = grade_task(task)
        results[task["task_id"]] = score

    return results


if __name__ == "__main__":
    results = run_all_tasks()

    for task_id, score in results.items():
        print(f"{task_id}: {score}")