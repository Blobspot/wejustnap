from task import Task

print("Test proportional rewards:")

print("\tCreate a task with proportional utility function, 100 effort required.")
my_task = Task(100)

print("\n\tTask's current utility (nothing if its not completed): " + str(my_task.get_utility()))
print("\tTask's remaining required effort: " + str(my_task.get_remaining_effort_needed()))

print("\n\tPlayer 1 contributes 50 effort to task.")
my_task.add_effort(1, 50)

print("\tTask's current utility (nothing if its not completed): " + str(my_task.get_utility()))
print("\tTask's remaining required effort: " + str(my_task.get_remaining_effort_needed()))

print("\n\tPlayer 2 contributes 50 effort to task.")
my_task.add_effort(2, 50)

print("\tTask's current utility (nothing if its not completed): " + str(my_task.get_utility()))
print("\tTask's remaining required effort: " + str(my_task.get_remaining_effort_needed()))

print("\n\tPlayer 3 contributes 300 effort to task.")
my_task.add_effort(3, 300)

print("\tTask's current utility (nothing if its not completed): " + str(my_task.get_utility()))
print("\tTask's remaining required effort: " + str(my_task.get_remaining_effort_needed()))

another_task = Task(-100)