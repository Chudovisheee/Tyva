import os
import sys
from database import get_db


def clear_screen():
    """Очистка экрана консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_admin_header():
    """Заголовок админ-панели"""
    print("╔═══════════════════════════════════════════════╗")
    print("║        АДМИНИСТРАТИВНАЯ ПАНЕЛЬ               ║")
    print("║       TyvaTravelPlanner v1.0                 ║")
    print("╚═══════════════════════════════════════════════╝")
    print()


def manage_places():
    """Управление туристическими местами"""
    db = get_db()

    while True:
        clear_screen()
        print_admin_header()
        print("📋 УПРАВЛЕНИЕ ТУРИСТИЧЕСКИМИ МЕСТАМИ")
        print("─" * 50)
        print("1. Просмотреть все места")
        print("2. Добавить новое место")
        print("3. Редактировать место")
        print("4. Удалить место")
        print("5. Поиск по категории")
        print("6. Вернуться в главное меню")
        print()

        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            # Просмотр всех мест
            places = db.get_all_places()
            print(f"\n📊 Всего мест в базе: {len(places)}")
            print("─" * 80)

            for place in places:
                print(f"ID: {place['id']:3d} | {place['name'][:30]:30} | {place['category']:15} | "
                      f"{place['city']:15} | {place['cost']:5d} руб")

            input("\nНажмите Enter для продолжения...")

        elif choice == '2':
            # Добавление нового места
            print("\n➕ ДОБАВЛЕНИЕ НОВОГО МЕСТА")
            print("─" * 40)

            name = input("Название места: ").strip()

            # Выбор категории
            categories = db.get_all_categories()
            print("\nДоступные категории:", ", ".join(categories))
            print("Или введите новую категорию")
            category = input("Категория: ").strip()

            description = input("Описание: ").strip()
            time_required = int(input("Время на посещение (часы, 1-8): ") or "2")
            cost = int(input("Стоимость посещения (руб): ") or "0")

            # Сезон
            print("\nСезонность (введите через запятую если несколько):")
            print("  Доступные: круглый год, лето, осень, зима, весна")
            season = input("Сезон: ").strip() or "круглый год"

            city = input("Город/район: ").strip()

            # Подтверждение
            print("\nПроверьте данные:")
            print(f"  Название: {name}")
            print(f"  Категория: {category}")
            print(f"  Город: {city}")
            print(f"  Стоимость: {cost} руб")
            print(f"  Время: {time_required} часов")
            print(f"  Сезон: {season}")

            confirm = input("\nДобавить это место? (да/нет): ").strip().lower()

            if confirm == 'да':
                place_id = db.add_new_place(name, category, description, time_required, cost, season, city)
                print(f"✅ Место успешно добавлено с ID: {place_id}")
            else:
                print("❌ Добавление отменено")

            input("\nНажмите Enter для продолжения...")

        elif choice == '3':
            # Редактирование места
            print("\n✏️ РЕДАКТИРОВАНИЕ МЕСТА")
            place_id = input("Введите ID места для редактирования: ").strip()

            if not place_id.isdigit():
                print("❌ Неверный ID")
                input("\nНажмите Enter для продолжения...")
                continue

            place = db.get_place_by_id(int(place_id))
            if not place:
                print(f"❌ Место с ID {place_id} не найдено")
                input("\nНажмите Enter для продолжения...")
                continue

            print(f"\nРедактирование: {place['name']}")
            print("─" * 40)
            print("Оставьте поле пустым, чтобы не изменять значение")

            new_name = input(f"Название [{place['name']}]: ").strip()
            new_category = input(f"Категория [{place['category']}]: ").strip()
            new_description = input(f"Описание [{place['description'][:50]}...]: ").strip()
            new_time = input(f"Время (часы) [{place['time_required']}]: ").strip()
            new_cost = input(f"Стоимость [{place['cost']}]: ").strip()
            new_season = input(f"Сезон [{place['season']}]: ").strip()
            new_city = input(f"Город [{place['city']}]: ").strip()

            # Обновление в базе (в реальном проекте нужно добавить метод update_place)
            print("\n⚠️ В этой версии редактирование не реализовано.")
            print("Для редактирования удалите и создайте заново.")

            input("\nНажмите Enter для продолжения...")

        elif choice == '4':
            # Удаление места
            print("\n🗑️ УДАЛЕНИЕ МЕСТА")
            place_id = input("Введите ID места для удаления: ").strip()

            if not place_id.isdigit():
                print("❌ Неверный ID")
                input("\nНажмите Enter для продолжения...")
                continue

            place = db.get_place_by_id(int(place_id))
            if not place:
                print(f"❌ Место с ID {place_id} не найдено")
                input("\nНажмите Enter для продолжения...")
                continue

            print(f"\nВы уверены, что хотите удалить место?")
            print(f"  Название: {place['name']}")
            print(f"  Категория: {place['category']}")
            print(f"  Город: {place['city']}")

            confirm = input("\nУдалить? (да/нет): ").strip().lower()

            if confirm == 'да':
                success = db.delete_place(int(place_id))
                if success:
                    print("✅ Место успешно удалено")
                else:
                    print("❌ Ошибка при удалении")
            else:
                print("❌ Удаление отменено")

            input("\nНажмите Enter для продолжения...")

        elif choice == '5':
            # Поиск по категории
            categories = db.get_all_categories()
            print("\n🔍 ПОИСК ПО КАТЕГОРИИ")
            print("Доступные категории:", ", ".join(categories))

            category = input("Введите категорию для поиска: ").strip()
            places = db.get_places_by_category(category)

            if not places:
                print(f"\n❌ Мест в категории '{category}' не найдено")
            else:
                print(f"\n📋 Найдено {len(places)} мест в категории '{category}':")
                print("─" * 80)

                for place in places:
                    print(f"  • {place['name']}")
                    print(f"    Город: {place['city']} | Стоимость: {place['cost']} руб | "
                          f"Время: {place['time_required']} ч")
                    print(f"    Описание: {place['description'][:80]}...")
                    print()

            input("\nНажмите Enter для продолжения...")

        elif choice == '6':
            break

        else:
            print("❌ Неверный выбор. Попробуйте снова.")
            input("\nНажмите Enter для продолжения...")


def manage_users():
    """Управление пользователями"""
    db = get_db()

    clear_screen()
    print_admin_header()
    print("👥 УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ")
    print("─" * 50)

    # Получаем статистику по пользователям
    stats = db.get_system_stats()

    print(f"Всего пользователей: {stats['total_users']}")
    print(f"Всего создано маршрутов: {stats['total_routes']}")
    print(f"Общая рассчитанная стоимость: {stats['total_money_calculated']} руб")

    # Получаем список пользователей
    db.cursor.execute("SELECT email, name, created_at FROM users ORDER BY created_at DESC")
    users = db.cursor.fetchall()

    if users:
        print("\n📋 СПИСОК ПОЛЬЗОВАТЕЛЕЙ:")
        print("─" * 60)
        for user in users:
            # Получаем количество маршрутов пользователя
            db.cursor.execute("SELECT COUNT(*) FROM routes WHERE user_email = ?", (user[0],))
            route_count = db.cursor.fetchone()[0]

            print(f"  Email: {user[0]}")
            print(f"  Имя: {user[1] or 'не указано'}")
            print(f"  Зарегистрирован: {user[2]}")
            print(f"  Создано маршрутов: {route_count}")
            print()

    input("\nНажмите Enter для возврата...")


def view_statistics():
    """Просмотр статистики системы"""
    db = get_db()

    clear_screen()
    print_admin_header()
    print("📊 СТАТИСТИКА СИСТЕМЫ")
    print("─" * 50)

    stats = db.get_system_stats()

    print(f"🎯 ОБЩАЯ СТАТИСТИКА:")
    print(f"   • Туристических мест: {stats['total_places']}")
    print(f"   • Зарегистрированных пользователей: {stats['total_users']}")
    print(f"   • Сгенерированных маршрутов: {stats['total_routes']}")
    print(f"   • Общая стоимость маршрутов: {stats['total_money_calculated']} руб")

    # Статистика по категориям
    print(f"\n🏷️ СТАТИСТИКА ПО КАТЕГОРИЯМ:")
    categories = db.get_all_categories()
    for category in categories:
        db.cursor.execute("SELECT COUNT(*) FROM places WHERE category = ?", (category,))
        count = db.cursor.fetchone()[0]
        db.cursor.execute("SELECT AVG(cost) FROM places WHERE category = ?", (category,))
        avg_cost = db.cursor.fetchone()[0] or 0
        print(f"   • {category}: {count} мест, средняя стоимость {avg_cost:.0f} руб")

    # Последние маршруты
    print(f"\n🕐 ПОСЛЕДНИЕ МАРШРУТЫ:")
    db.cursor.execute('''
        SELECT r.id, r.user_email, r.total_days, r.total_cost, r.created_at, 
               COUNT(json_each.value) as places_count
        FROM routes r, json_each(r.places_ids)
        GROUP BY r.id
        ORDER BY r.created_at DESC
        LIMIT 5
    ''')
    recent_routes = db.cursor.fetchall()

    if recent_routes:
        for route in recent_routes:
            print(f"   • Маршрут #{route[0]}: {route[2]} дней, {route[3]} руб, "
                  f"{route[4]} мест, пользователь {route[1]}")
    else:
        print("   • Маршрутов пока нет")

    # Самые популярные места
    print(f"\n⭐ САМЫЕ ПОПУЛЯРНЫЕ МЕСТА (по частоте в маршрутах):")
    # В реальном проекте нужен более сложный запрос для подсчёта популярности

    input("\n\nНажмите Enter для возврата...")


def backup_database():
    """Создание резервной копии базы данных"""
    import shutil
    from datetime import datetime

    clear_screen()
    print_admin_header()
    print("💾 СОЗДАНИЕ РЕЗЕРВНОЙ КОПИИ БАЗЫ ДАННЫХ")
    print("─" * 50)

    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'tyva_db_backup_{timestamp}.db')

    try:
        # Копируем файл базы данных
        shutil.copy2('tyva_tourism.db', backup_file)

        # Создаем SQL-дампа (простой вариант)
        dump_file = os.path.join(backup_dir, f'tyva_db_dump_{timestamp}.sql')
        db = get_db()

        with open(dump_file, 'w', encoding='utf-8') as f:
            # Запись структуры и данных
            for line in db.conn.iterdump():
                f.write(f'{line}\n')

        print(f"✅ Резервная копия создана успешно!")
        print(f"   Файл БД: {backup_file}")
        print(f"   SQL-дамп: {dump_file}")

        # Показываем список бэкапов
        backups = [f for f in os.listdir(backup_dir) if f.startswith('tyva_db_')]
        print(f"\n📂 Всего резервных копий: {len(backups)}")

    except Exception as e:
        print(f"❌ Ошибка при создании резервной копии: {e}")

    input("\nНажмите Enter для возврата...")


def admin_main():
    """Главное меню админ-панели"""
    while True:
        clear_screen()
        print_admin_header()
        print("ГЛАВНОЕ МЕНЮ АДМИНИСТРАТОРА")
        print("─" * 40)
        print("1. 📋 Управление туристическими местами")
        print("2. 👥 Управление пользователями")
        print("3. 📊 Просмотр статистики системы")
        print("4. 💾 Создание резервной копии БД")
        print("5. 🚪 Выход из админ-панели")
        print("6. 🔄 Перезагрузить базу данных (сброс к демо-данным)")
        print()

        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            manage_places()
        elif choice == '2':
            manage_users()
        elif choice == '3':
            view_statistics()
        elif choice == '4':
            backup_database()
        elif choice == '5':
            print("\n👋 Выход из админ-панели...")
            break
        elif choice == '6':
            # Перезагрузка БД с демо-данными
            confirm = input("\n⚠️ ВНИМАНИЕ: Все текущие данные будут удалены и заменены демо-данными!\n"
                            "Продолжить? (да/нет): ").strip().lower()
            if confirm == 'да':
                # Удаляем файл БД и создаём заново
                db = get_db()
                db.close()

                if os.path.exists('tyva_tourism.db'):
                    os.remove('tyva_tourism.db')

                # Переимпортируем для создания новой БД
                from database import Database
                db = Database()
                db.close()

                print("✅ База данных перезагружена с демо-данными")
                input("\nНажмите Enter для продолжения...")
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    # Проверка пароля для доступа к админке (простой вариант)
    password = input("Введите пароль администратора: ").strip()

    # Простой пароль для демонстрации
    if password == "admin123":
        admin_main()
    else:
        print("❌ Неверный пароль. Доступ запрещён.")
        input("\nНажмите Enter для выхода...")