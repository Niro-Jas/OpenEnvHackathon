from env.environment import CivicEnv

def easy_task():
    """Single issue, clear solution"""
    env = CivicEnv()
    state = env.reset()

    return {
        "task_id": "easy_1",
        "state": state,
        "description": "Handle a single civic issue with correct department and priority"
    }


def medium_task():
    """Multiple steps, limited resources"""
    env = CivicEnv()
    state = env.reset()

    # Make it slightly harder
    state["resources_available"] = 1

    return {
        "task_id": "medium_1",
        "state": state,
        "description": "Solve issue with limited resources"
    }


def hard_task():
    """High severity + tricky decision"""
    env = CivicEnv()
    state = env.reset()

    # Make it challenging
    state["severity"] = 5
    state["days_pending"] = 7
    state["resources_available"] = 1

    return {
        "task_id": "hard_1",
        "state": state,
        "description": "Handle critical issue with minimal resources"
    }
if __name__ == "__main__":
    print(easy_task())
    print(medium_task())
    print(hard_task())