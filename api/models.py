from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

TASK_STATUS = (
    ('To Do', 'To Do'),
    ('In Progress', 'In Progress'),
    ('Done', 'Done'),
    ('Hold', 'Hold')
)

TASK_PRIORITY = (
    ('Highest', 'Higest'),
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
    ('Lowest', 'Lowest')
)

TASK_TYPE = (
    ('Story', 'Story'),
    ('Bug', 'Bug'),
    ('Epic', 'Epic')
)

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        super().save()

class Board(TimeStamp): # project
    title = models.CharField(max_length=255)
    visibility = models.BooleanField(default=True)
    description = models.TextField()

    members = models.ManyToManyField(User, related_name='boards')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def board_short_name(self):
        return "".join(list(map(lambda x: x[0], self.title.split(" "))))


class Column(TimeStamp):
    title = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=0)

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

class Task(TimeStamp):
    title = models.CharField(max_length=255)
    task_id = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=30, choices=TASK_STATUS)
    priority = models.CharField(max_length=30, choices=TASK_PRIORITY, default='Medium')
    
    position = models.PositiveIntegerField(default=0)

    task_type = models.CharField(max_length=15, choices=TASK_TYPE, default='Task')

    deadline = models.DateTimeField()

    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='tasks')
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.task_id:
            board_name = self.column.board.board_short_name()
            self.task_id = board_name + "-" + str(self.pk)
        
        super().save(*args, **kwargs)

    



