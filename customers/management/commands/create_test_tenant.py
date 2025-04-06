import sys
from datetime import date, datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from customers.models import Client, Domain # Импортируем ваши модели

class Command(BaseCommand):
    help = 'Создает тестового клиента (тенанта) с указанным именем схемы, именем клиента и доменом.'

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help='Уникальное имя схемы PostgreSQL (например, client_test).')
        parser.add_argument('tenant_name', type=str, help='Название компании клиента (например, Тестовый Клиент).')
        parser.add_argument('domain_url', type=str, help='Домен или субдомен для доступа (например, test.localhost или test.127.0.0.1.nip.io).')
        parser.add_argument(
            '--paid_until',
            type=str,
            default=date(2099, 12, 31).strftime('%Y-%m-%d'), # По умолчанию очень далекая дата
            help='Дата окончания оплаты в формате YYYY-MM-DD.'
        )
        parser.add_argument(
            '--on_trial',
            action='store_true', # Если флаг указан, будет True
            help='Установить флаг пробного периода (on_trial).'
        )

    @transaction.atomic # Используем транзакцию для атомарности
    def handle(self, *args, **options):
        schema_name = options['schema_name']
        tenant_name = options['tenant_name']
        domain_url = options['domain_url']
        on_trial = options['on_trial']
        paid_until_str = options['paid_until']

        try:
            paid_until_date = datetime.strptime(paid_until_str, '%Y-%m-%d').date()
        except ValueError:
            raise CommandError("Неверный формат даты для --paid_until. Используйте YYYY-MM-DD.")

        # Проверка на существование
        if Client.objects.filter(schema_name=schema_name).exists():
            raise CommandError(f"Тенант со схемой '{schema_name}' уже существует.")
        if Domain.objects.filter(domain=domain_url).exists():
            raise CommandError(f"Домен '{domain_url}' уже используется.")

        try:
            # Создаем тенанта
            # auto_create_schema=True (из вашей модели) должен сработать при .save()
            tenant = Client(
                schema_name=schema_name,
                name=tenant_name,
                paid_until=paid_until_date,
                on_trial=on_trial
                # auto_create_schema=True # Убедитесь что это поле есть в модели
            )
            tenant.save()
            self.stdout.write(self.style.SUCCESS(f"Тенант '{tenant.name}' со схемой '{tenant.schema_name}' успешно создан."))

            # Создаем домен
            domain = Domain(
                domain=domain_url,
                tenant=tenant,
                is_primary=True
            )
            domain.save()
            self.stdout.write(self.style.SUCCESS(f"Домен '{domain.domain}' успешно создан для тенанта '{tenant.name}'."))

        except Exception as e:
            # Отлавливаем любые другие ошибки при создании
            # Удаляем тенанта, если домен не создался (транзакция откатится, но для чистоты)
            if 'tenant' in locals() and tenant.pk:
                 # Попытка удалить схему, если она успела создаться
                 try:
                     # django-tenants должен удалить схему при удалении объекта
                     tenant.delete()
                     self.stdout.write(self.style.WARNING(f"Откат: Удален тенант '{tenant.name}' из-за ошибки."))
                 except Exception as del_e:
                     self.stdout.write(self.style.ERROR(f"Критическая ошибка при откате создания тенанта: {del_e}"))

            raise CommandError(f"Ошибка при создании тенанта или домена: {e}")
