import random


class CivicEnv:
    def __init__(self):
        self.current_state = None
        self.steps = 0
        self.max_steps = 3

        # Issue types
        self.issue_types = ["pothole", "garbage", "water_leak", "streetlight"]

        # Correct department mapping
        self.department_map = {
            "pothole": "road",
            "garbage": "sanitation",
            "water_leak": "water",
            "streetlight": "electric"
        }

    def reset(self):
        """Initialize a new issue"""
        self.steps = 0

        self.current_state = {
            "issue_type": random.choice(self.issue_types),
            "severity": random.randint(1, 5),
            "days_pending": random.randint(1, 7),
            "resources_available": random.randint(1, 3)
        }

        return self.current_state

    def step(self, action):
        """
        Action format:
        {
            "department": str,
            "priority": str,   # low / medium / high
            "resources": int
        }
        """

        self.steps += 1
        reward = 0.0

        issue = self.current_state["issue_type"]
        severity = self.current_state["severity"]
        resources_available = self.current_state["resources_available"]

        # ✅ 1. Department correctness
        if action.get("department") == self.department_map[issue]:
            reward += 0.3

        # ✅ 2. Priority correctness
        if severity >= 4 and action.get("priority") == "high":
            reward += 0.3
        elif severity == 3 and action.get("priority") == "medium":
            reward += 0.2
        elif severity <= 2 and action.get("priority") == "low":
            reward += 0.2

        # ✅ 3. Resource allocation
        used_resources = action.get("resources", 0)

        if used_resources <= resources_available:
            reward += 0.2
        else:
            reward -= 0.1  # penalty

        # ✅ 4. Faster resolution bonus
        if self.steps == 1:
            reward += 0.2

        # Clamp reward between 0 and 1
        reward = max(0.0, min(1.0, reward))

        done = self.steps >= self.max_steps

        return self.current_state, reward, done, {}

    def get_state(self):
        """Return current state"""
        return self.current_state


# 🔍 Test run
if __name__ == "__main__":
    env = CivicEnv()

    state = env.reset()
    print("Initial State:", state)

    action = {
        "department": "road",
        "priority": "high",
        "resources": 2
    }

    next_state, reward, done, _ = env.step(action)

    print("Action:", action)
    print("Reward:", reward)
    print("Done:", done)