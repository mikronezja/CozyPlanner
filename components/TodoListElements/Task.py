# Task defined in a to-do list
# Later displayed in EisenHower Matrix

class Task: 
    def __init__(self, name, desc):
        self.name = name 
        self.desc = desc 
        self.completed = False # domyslnie tworzony ma wartosc False
    def task_completed(self):
        self.completed = True
    def task_not_completed(self):
        self.completed = False