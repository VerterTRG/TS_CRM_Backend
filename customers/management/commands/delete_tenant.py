import sys
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from customers.models import Client # Импортируем вашу модель Client

class Command(BaseCommand):
    help = 'Удаляет клиента (тенанта) и его схему по имени схемы.'

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help='Имя схемы тенанта для удаления (например, test_client).')
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Удалить без запроса подтверждения (ИСПОЛЬЗУЙТЕ С ОСТОРОЖНОСТЬЮ!).'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        schema_name = options['schema_name']
        no_input = options['no_input']

        try:
            tenant = Client.objects.get(schema_name=schema_name)
        except Client.DoesNotExist:
            raise CommandError(f"Тенант со схемой '{schema_name}' не найден.")

        self.stdout.write(self.style.WARNING(f"Вы собираетесь удалить тенанта '{tenant.name}' со схемой '{schema_name}'."))
        self.stdout.write(self.style.WARNING(">>> ВНИМАНИЕ: Это действие НЕОБРАТИМО! <<<"))
        self.stdout.write(self.style.WARNING(">>> Будет удалена схема PostgreSQL '{schema_name}' и ВСЕ ДАННЫЕ внутри нее! <<<"))

        confirmation = 'yes' if no_input else None
        if not no_input:
            confirmation = input("Чтобы подтвердить удаление, введите 'yes': ")

        if confirmation == 'yes':
            try:
                # Получаем pk и имя перед удалением, так как объект будет недоступен
                tenant_pk = tenant.pk
                tenant_name = tenant.name

                # Удаление объекта тенанта вызовет удаление схемы (см. ниже)
                tenant.delete()

                self.stdout.write(self.style.SUCCESS(f"Тенант '{tenant_name}' (PK: {tenant_pk}) и его схема '{schema_name}' успешно удалены."))
            except Exception as e:
                 raise CommandError(f"Ошибка при удалении тенанта '{schema_name}': {e}")
        else:
            self.stdout.write(self.style.NOTICE("Удаление отменено."))
