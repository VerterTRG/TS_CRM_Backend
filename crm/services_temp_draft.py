from typing import Optional
from django.db import IntegrityError, transaction
from django.utils import timezone
from time import sleep


# Импорт модели счетчиков
from .models import GaplessSequence

def allocate_gapless_number(
    name: str,
    tenant: Optional[str] = None,
    year: Optional[int] = None,
    user_initials: Optional[str] = None,
    max_retries: int = 3
) -> int:
    """
    Возвращает следующий gapless номер в последовательности, определяемой (name, tenant, year, user_initials).
    Если требуется нумерация в виде 2025/AB/0001 — используйте year=2025 и user_initials='AB'.
    Должна вызываться внутри transaction.atomic() или сама использует atomic. Реализована на ORM:
      - использует select_for_update() для блокировки строки;
      - при отсутствии строки — пытается создать;
      - при коллизиях делает несколько попыток (IntegrityError -> retry).
    Пример вызова:
      with transaction.atomic():
          number = allocate_gapless_number('invoice', tenant='tenant_42', year=2025)
          Invoice.objects.create(number=number, ...)
    """
    if year is None:
        year = timezone.now().year

    for attempt in range(max_retries):
        try:
            with transaction.atomic():
                # get_or_create + select_for_update — безопасно внутри atomic с ретраем на IntegrityError
                obj, created = GaplessSequence.objects.select_for_update().get_or_create(
                    name=name,
                    tenant=tenant,
                    year=year,
                    user_initials=user_initials,
                    defaults={'value': 0}
                )
                # Инкрементируем и сохраняем
                obj.value = obj.value + 1
                obj.save(update_fields=['value'])
                return obj.value
        except IntegrityError:
            # В случае конкурентного создания — делаем небольшую паузу и повторяем
            if attempt + 1 >= max_retries:
                raise
            sleep(0.05)

    # Если не вернули внутри цикла — поднимаем исключение
    raise RuntimeError("Не удалось выделить gapless номер после нескольких попыток")

# def allocate_gapless_number(seq_name: str) -> int:
#     """
#     Возвращает следующий gapless номер для последовательности seq_name.
#     Должна вызываться внутри transaction.atomic (или сама использует atomic).
#     Реализовано через простую таблицу crm_gapless_sequence:
#       (name text PRIMARY KEY, value bigint NOT NULL)
#     Таблица будет создана при первом вызове, если отсутствует.
#     """
#     with transaction.atomic():
#         with connection.cursor() as cur:
#             # Создадим таблицу, если её нет (DDL вне основной логики — безопасно делать редко)
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS crm_gapless_sequence (
#                     name TEXT PRIMARY KEY,
#                     value BIGINT NOT NULL
#                 )
#             """)
#             # Попытка вставить начальное значение (если строки ещё нет)
#             cur.execute(
#                 "INSERT INTO crm_gapless_sequence (name, value) VALUES (%s, 0) ON CONFLICT (name) DO NOTHING",
#                 [seq_name],
#             )
#             # Блокируем строку и читаем текущее значение
#             cur.execute(
#                 "SELECT value FROM crm_gapless_sequence WHERE name = %s FOR UPDATE",
#                 [seq_name],
#             )
#             row = cur.fetchone()
#             current = row[0] if row else 0
#             next_val = current + 1
#             # Обновляем значение
#             cur.execute(
#                 "UPDATE crm_gapless_sequence SET value = %s WHERE name = %s",
#                 [next_val, seq_name],
#             )
#             return next_val