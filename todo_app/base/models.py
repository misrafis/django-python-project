from django.db import models
from django.contrib.auth.models import User


# Model (wygląd tabeli w bazie danych) zadania
class Task(models.Model):
    # Pole użytkownik jako klucz obcy po użytkowniku z tabeli User, która standardowo w django odpowiada za użytkowników
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Tytuł zadania jako pole znaków o długości znaków 200
    title = models.CharField(max_length=200)
    # Opis zadania jako pole tekstowe
    description = models.TextField()
    # Czy zadanie zostało wykonane jako Boolean
    complete = models.BooleanField(default=False)
    # Data utworzenia zadania
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Sortowanie zadania po statusie wykonania - wykonane zadania będą na dole tabeli
    class Meta:
        ordering = ['complete']
