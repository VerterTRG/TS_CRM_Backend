# Это можно сделать в management-команде, скрипте, или даже в shell_plus / shell
from django.apps import apps
from django.db.models.fields import Field # Для проверки, что это поле данных

def find_models_with_tmp_fields():
    """
    Находит модели Django, у которых есть поля,
    имена которых или имена колонок в БД заканчиваются на '_tmp'.
    """
    models_found = []
    tables_found = set()

    # Получаем все зарегистрированные модели в проекте
    all_models = apps.get_models()

    for model in all_models:
        model_meta = model._meta
        found_in_model = False
        # Перебираем все поля, определенные непосредственно в этой модели
        # (local_fields не включает поля из родительских классов или ManyToMany)
        # Используем get_fields() для более полного охвата, но фильтруем
        for field in model_meta.get_fields():
            # Убедимся, что это поле имеет колонку в БД
            # Простые поля, FK, OneToOne имеют 'column'
            # ManyToMany и обратные связи - нет
            if hasattr(field, 'column') and field.column: # type: ignore
                # Проверяем имя поля в Django И имя колонки в БД
                field_name = field.name
                column_name = field.column # type: ignore
                if field_name.endswith('_tmp') or column_name.endswith('_tmp'):
                    models_found.append(model)
                    tables_found.add(model_meta.db_table)
                    found_in_model = True
                    break # Нашли одно поле в модели, переходим к следующей

    print("--- Поиск завершен ---")
    if models_found:
        print("Модели с полями '*_tmp':")
        for m in models_found:
            print(f"- {m.__module__}.{m.__name__} (таблица: {m._meta.db_table})")
        print("\nИмена таблиц с колонками '*_tmp':")
        for t in sorted(list(tables_found)):
            print(f"- {t}")
    else:
        print("Модели/таблицы с полями/колонками '*_tmp' не найдены.")

    return models_found, tables_found

# --- Пример вызова ---
if __name__ == '__main__': # Если запускаем как скрипт
    # Убедитесь, что Django настроен перед вызовом apps.get_models()
    # Например, через manage.py shell или в management command
    # import django
    # django.setup()
    find_models_with_tmp_fields()