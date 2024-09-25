from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100, default='Unknown')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)  # Assuming role with id=1 exists
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)  # Assuming department with id=1 exists

    def __str__(self):
        return self.name

from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_tasks')  # HoD or other
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)  # New field for deadline
    def __str__(self):
        return self.title

    @property
    def is_completed_on_time(self):
        """ Check if the task was completed on or before the deadline. """
        return self.completed_at <= self.deadline if self.completed_at and self.deadline else False

    @property
    def time_taken(self):
        """ Calculate the time taken to complete the task. """
        return (self.completed_at - self.created_at).total_seconds() / 3600 if self.completed_at else None
