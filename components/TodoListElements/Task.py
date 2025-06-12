# Task defined in a to-do list
# Later displayed in EisenHower Matrix

class Task: 
    def __init__(self, name, desc, importance, urgency):
        self.name = name 
        self.desc = desc 
        self.completed = False # default value is false
        self.importance = importance # the importance of a task
        self.urgency = urgency # urgency of a task

    def task_completed(self):
        self.completed = True
    def task_not_completed(self):
        self.completed = False