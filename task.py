class Task:
    def __init__(self, required_effort):
        self.required_effort = required_effort
        self.effort_contributed = 0  # Initialize total contributed effort

    def add_effort(self, effort):
        """Add effort to the task and accumulate the total."""
        self.effort_contributed += effort

    def get_total_effort_contributed(self):
        """Return the total effort contributed so far."""
        return self.effort_contributed

    def is_complete(self):
        """Check if the task is complete."""
        return self.effort_contributed >= self.required_effort

    def remaining_effort(self):
        """Return the remaining effort needed to complete the task."""
        return max(self.required_effort - self.effort_contributed, 0)
