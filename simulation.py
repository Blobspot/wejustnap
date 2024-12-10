import random
from player import Player
from task import Task
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from multiprocessing import Pool

# Simulation parameters
num_simulations = 20
max_team_size = 9
max_tasks = 9


# calculate ideal social welfare
def calculate_ideal_social_welfare(players, tasks):
    total_available_effort = sum(player.get_effort_allocation() for player in players)
    sorted_tasks = sorted(tasks, key=lambda t: t.required_effort, reverse=True)

    ideal_sw = 0
    for task in sorted_tasks:
        if total_available_effort <= 0:
            break  # No more effort to allocate

        effort_to_allocate = min(task.required_effort, total_available_effort)
        ideal_sw += effort_to_allocate
        total_available_effort -= effort_to_allocate

    return ideal_sw


def self_organized_effort(players, tasks):
    for player in players:
        # Shuffle assigned tasks
        assigned_tasks = player.get_assigned_tasks()
        random.shuffle(assigned_tasks)

        for task in assigned_tasks:
            remaining_player_effort = player.get_remaining_effort()
            if remaining_player_effort > 0:
                # Add slight randomness to effort allocation
                effort_to_add = min(
                    task.remaining_effort(),
                    random.randint(1, remaining_player_effort)
                )
                task.add_effort(effort_to_add)



# Runs Simulation
def run_simulation(args):
    n, m = args
    best_SW, worst_SW = 0, float('inf')
    best_TH, worst_TH = 0, float('inf')

    players = [
        Player(effort_allocation=5, skills={"developer": 1.0}) for _ in range(n)
    ]
    tasks = [
        Task(required_effort=30 + 5 * i) for i in range(m)
    ]

    for _ in range(num_simulations):
        # Reset task efforts
        for task in tasks:
            task.effort_contributed = 0

        # Assign tasks to players
        for player in players:
            player.assign_tasks(tasks)

        # Simulate 2 weeks of work
        for _ in range(14):
            self_organized_effort(players, tasks)

        SW = sum(task.get_total_effort_contributed() for task in tasks)
        TH = sum(task.required_effort if task.is_complete() else 0 for task in tasks)

        # Track best and worst outcomes
        best_SW = max(best_SW, SW)  # Maximize social welfare
        worst_SW = min(worst_SW, SW)  # Minimize social welfare
        best_TH = max(best_TH, TH)  # Maximize task completion
        worst_TH = min(worst_TH, TH)  # Minimize task completion

    # Calculate ideal SW
    ideal_SW = calculate_ideal_social_welfare(players, tasks)

    # Normalize and calculate PoS and PoA
    PoS_SW = ideal_SW / best_SW
    PoA_SW = ideal_SW / worst_SW
    PoS_TH = ideal_SW / best_TH
    PoA_TH = ideal_SW / worst_TH

    return {
        "Team Size (n)": n,
        "Tasks (m)": m,
        "Best SW": best_SW,
        "Worst SW": worst_SW,
        "Best TH": best_TH,
        "Worst TH": worst_TH,
        "PoS SW": PoS_SW,
        "PoA SW": PoA_SW,
        "PoS TH": PoS_TH,
        "PoA TH": PoA_TH
    }


# Run in paralel to decrease run time
if __name__ == "__main__":
    pool = Pool()
    params = [(n, m) for n in range(1, max_team_size + 1) for m in range(1, max_tasks + 1)]
    results = pool.map(run_simulation, params)
    pool.close()
    pool.join()

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Plot Box and whiskers graphs
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Team Size (n)", y="PoS SW", data=df)
    plt.title("Price of Stability (PoS) for Social Welfare vs. Team Size")
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Team Size (n)", y="PoA SW", data=df)
    plt.title("Price of Anarchy (PoA) for Social Welfare vs. Team Size")
    plt.show()

    # Plot Heatmap Results
    heatmap_data_pos_th = df.pivot_table(index="Tasks (m)", columns="Team Size (n)", values="PoS TH")
    sns.heatmap(heatmap_data_pos_th, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'PoS TH'})
    plt.title("Price of Stability (PoS) for Threshold Completed")
    plt.xlabel("Team Size (n)")
    plt.ylabel("Number of Tasks (m)")
    plt.show()

    heatmap_data_poa_th = df.pivot_table(index="Tasks (m)", columns="Team Size (n)", values="PoA TH")
    sns.heatmap(heatmap_data_poa_th, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'PoA TH'})
    plt.title("Price of Anarchy (PoA) for Threshold Completed")
    plt.xlabel("Team Size (n)")
    plt.ylabel("Number of Tasks (m)")
    plt.show()
