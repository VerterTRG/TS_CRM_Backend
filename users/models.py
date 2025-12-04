from django.contrib.auth.models import AbstractUser
from django.db import models
from customers.models import Client

class CustomUser(AbstractUser):
    # Унаследует поля username, first_name, last_name, email, is_staff и т.д.
    # Добавьте ваши поля:
    email = models.EmailField(unique=True) # Сделать email уникальным и основным логином
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True) # Пример связи с тенантом
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # ... другие ваши поля

    # Если используете email как основной логин вместо username:
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Или пустой список, если email не нужен

    def __str__(self):
        return self.username # или email если он основной
    
    @property
    def client_name(self) -> str | None:
        if self.client:
            return self.client.name
        return None # Возвращаем None, если клиент не привязан
    
    @property
    def schema_name(self) -> str | None:
        # Убедитесь, что у модели Client есть поле 'schema_name'
        return self.client.schema_name if self.client else None