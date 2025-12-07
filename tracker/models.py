from django.db import models
from django.conf import settings

class Task(models.Model):
    class Status(models.TextChoices):
        TODO="TODO", "To do"
        IN_PROGRESS="IN_PROGRESS","In progress"
        DONE="DONE","Done"

    class Priority(models.TextChoices):
        LOW="LOW","Low"
        MEDIUM="MEDIUM","Medium"
        HIGH="HIGH","High"

    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)

    status=models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    priority=models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    due_date=models.DateField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    class Meta:
        ordering=["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.status})"
    
class Habit(models.Model):
    class Frequency(models.TextChoices):
        DAILY="DAILY",'Daily'
        WEEKLY="WEEKLY","Weekly"


    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )

    name=models.CharField(max_length=255)
    frequency=models.CharField(
        max_length=20,
        choices=Frequency.choices,
        default=Frequency.DAILY,
    )

    target_per_week=models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Used if frequency is weekly",
    )

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self)->str:
        return self.name
    
class HabitLog(models.Model):
    habit=models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    date=models.DateField()


    class Meta:
        unique_together=("habit","date")
        ordering=["-date"]

    def __str__(self)->str:
        return f"{self.habit.name} @ {self.date}"