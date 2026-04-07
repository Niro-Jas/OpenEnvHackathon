import os
import json
from env.environment import CivicEnv
from env.tasks import easy_task, medium_task, hard_task
from openai import OpenAI

# Load environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )
else:
    client = None


def get_action_from_llm(state):
    # ✅ If no API → use fallback directly
    if client is None:
        return {
            "department": "road",
            "priority": "medium",
            "resources": 1
        }

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": f"""
State:
{json.dumps(state)}

Return JSON with:
department, priority, resources
"""
            }],
            temperature=0
        )

        content = response.choices[0].message.content
        action = json.loads(content)

    except Exception:
        action = {
            "department": "road",
            "priority": "medium",
            "resources": 1
        }

    return action


def run_task(task):
    env = CivicEnv()
    env.current_state = task["state"]

    print("[START]")
    print(f"task_id: {task['task_id']}")

    done = False
    final_reward = 0

    while not done:
        state = env.get_state()

        # ✅ CORRECT CALL
        action = get_action_from_llm(state)

        next_state, reward, done, _ = env.step(action)
        final_reward = reward

        print("\n[STEP]")
        print(f"action: {action}")
        print(f"reward: {reward}")

    print("\n[END]")
    print(f"final_score: {final_reward}")
    print("\n----------------------\n")


def main():
    tasks = [easy_task(), medium_task(), hard_task()]

    for task in tasks:
        run_task(task)


if __name__ == "__main__":
    main()