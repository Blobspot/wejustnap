
import random

class Task:

    def __init__(self, required_effort, utility_func="proportional", skills_required={"developer":1.0}):

        self.function_map = {
            "proportional": self.__proportional_utility_func,
            "winner_takes_all": self.__winner_takes_all_utility_func,
        }

        if required_effort < 1:
            raise ValueError("\'required_effort\' must be greater than 0")
        
        self.skills_required = skills_required
        self.required_effort = required_effort
        self.utility_if_completed = required_effort   # This could change perhaps?
        self.effort_completed = 0
        self.utility_func = self.function_map[utility_func]
        self.effort_tracker = {}


    # Gives out points to players proportional to contributions
    # It will reward even those players that contributed after the task was complete
    def __proportional_utility_func(self):
        players_utility = {}

        for player in self.effort_tracker.keys():
            players_utility[player] = (self.effort_tracker[player] / self.effort_completed) * self.utility_if_completed

        return players_utility
    
    # Gives all points to the player that contributed the most
    # If there are any ties, one will be randomly selected and given all the points
    # Returns a dictionary mapping player id's to utility earned
    def __winner_takes_all_utility_func(self):
        highest_contributers = self.__highest_contributers()
        if len(highest_contributers) > 1:
            rand_index = random.randint(0, len(highest_contributers)-1)
            return {highest_contributers[rand_index]: self.utility_if_completed}
        else:
            return {highest_contributers[0]: self.utility_if_completed}
        
    def get_utility(self):
        if self.__check_task_complete() == True:
            return self.utility_func()
        else:
            return {}
    
    def add_effort(self, effort_adder_player_id, amount_of_effort, player_skills=["developer"]):

        skill_percentage = 0
        # Assumes player skills is a list
        for skill in player_skills:
            skill_percentage += self.skills_required[skill]
        
        actual_contributed_effort = amount_of_effort * skill_percentage

        self.effort_completed += actual_contributed_effort
        


        if effort_adder_player_id in self.effort_tracker.keys():
            self.effort_tracker[effort_adder_player_id] += actual_contributed_effort
        else:
            self.effort_tracker[effort_adder_player_id] = actual_contributed_effort

    def __highest_contributers(self):
        effort_list = self.effort_tracker.values()
        highest_contribution = max(effort_list)
        highest_contributors = []

        for player in self.effort_tracker.keys():
            if self.effort_tracker[player] == highest_contribution:
                highest_contributors.append(player)
        
        return highest_contributors
        
    def __check_task_complete(self):
        if self.effort_completed >= self.required_effort:
            return True
        else:
            return False
    
    def get_remaining_effort_needed(self):
        remaining = self.required_effort - self.effort_completed
        if remaining >= 0:
            return remaining
        else:
            return 0
    
    
