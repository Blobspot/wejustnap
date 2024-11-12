from player import Player
from task import Task
import random

# used to create and keep track of different tasks
class SimulatedTask:
    def __init__(self, required_effort):
        self.task = Task(required_effort=required_effort)
        self.required_effort = required_effort
        self.effort_contributed = 0

    def add_effort(self, effort):
        self.effort_contributed += effort

    def is_complete(self):
        return self.effort_contributed >= self.required_effort

    def remaining_effort(self):
        return max(self.required_effort - self.effort_contributed, 0)


# create a set of tasks with varying required efforts
tasks = [
    SimulatedTask(required_effort=10),
    SimulatedTask(required_effort=15),
    SimulatedTask(required_effort=20),
    SimulatedTask(required_effort=25)
]

# create players with different effort allocations and skills
players = [
    Player(effort_allocation=5, skills={"developer": 1.0}),
    Player(effort_allocation=3, skills={"developer": 1.0}),
    Player(effort_allocation=4, skills={"developer": 1.0})
]

# assign tasks to players
for player in players:
    player.assign_tasks([t.task for t in tasks])

# simulate players choosing tasks and adding effort 14 times
for iteration in range(1, 15):
    print(f"--- Iteration {iteration} ---")

    for player in players:
        # randomly select a task from the assigned tasks
        task = random.choice(player.get_assigned_tasks())
        simulated_task = next(t for t in tasks if t.task == task)

        # randomly determine how much effort the player will add (within their remaining capacity)
        remaining_player_effort = player.get_remaining_effort()
        if remaining_player_effort > 0:
            effort_to_add = random.randint(1, remaining_player_effort)
            simulated_task.add_effort(effort_to_add)

    # print out the current status of each task's remaining effort
    for idx, simulated_task in enumerate(tasks, start=1):
        print(f"Task {idx}: Effort needed for completion: {simulated_task.remaining_effort()}")

# final report
print("\n--- Final Report ---")
for idx, simulated_task in enumerate(tasks, start=1):
    if simulated_task.is_complete():
        print(f"Task {idx} is complete.")
    else:
        print(f"Task {idx} is incomplete. Effort still needed: {simulated_task.remaining_effort()}")
