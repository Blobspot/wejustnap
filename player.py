from task import Task
from uuid import uuid4


class Player():
    # constructor
    def __init__(self, assigned_tasks=[], effort_allocation=1, skills={"developer": 1.0}):
        if effort_allocation < 1:
            raise ValueError("'effort_allocation' must be greater than 0")
        if len(skills) < 1:
            raise ValueError("'skills' cannot be empty")

        self.__assigned_tasks = assigned_tasks
        self.__effort_allocation = effort_allocation
        self.__skills = skills

        # TODO: are we wanting this to get auto-generated or passed in? leaving auto for now
        self.id = uuid4()
        self.__effort_expended = 0
        self.__daily_effort_report = {
            'mon': 0,
            'tue': 0,
            'wed': 0,
            'thu': 0,
            'fri': 0,
        }

    # assign tasks to the player
    # tasks: a list() of >= 1 Task objects
    def assign_tasks(self, tasks):
        if not isinstance(tasks, list):
            raise ValueError("Object passed to 'tasks' parameter must be a list with Task object(s)")
        for i in tasks:
            if not isinstance(i, Task):
                raise ValueError("An object in the 'tasks' list is not a Task: " + str(type(i)))
        self.__assigned_tasks.extend(tasks)

    # getters
    def get_assigned_tasks(self):
        return self.__assigned_tasks

    def get_remaining_effort(self):
        return self.__effort_allocation - self.__effort_expended

    def get_effort_report(self):
        return self.__daily_effort_report

    def get_effort_allocation(self):
        return self.__effort_allocation
