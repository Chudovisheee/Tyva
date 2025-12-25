import os
import sys
import time
from datetime import datetime
from database import get_db
from route_generator import RouteGenerator
from export import ExportManager


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_logo():
    logo = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     ████████╗██╗   ██╗██╗   ██╗ █████╗                      ║
    ║     ╚══██╔══╝╚██╗ ██╔╝██║   ██║██╔══██╗                     ║
    ║        ██║    ╚████╔╝ ██║   ██║███████║                     ║
    ║        ██║     ╚██╔╝  ╚██╗ ██╔╝██╔══██║                     ║
    ║        ██║      ██║    ╚████╔╝ ██║  ██║                     ║
    ║        ╚═╝      ╚═╝     ╚═══╝  ╚═╝  ╚═╝                     ║
    ║                                                              ║
    ║    ████████╗██████╗  █████╗ ██╗    ██╗███████╗██╗           ║
    ║    ╚══██╔══╝██╔══██╗██╔══██╗██║    ██║██╔════╝██║           ║
    ║       ██║   ██████╔╝███████║██║ █╗ ██║█████╗  ██║           ║
    ║       ██║   ██╔══██╗██╔══██║██║███╗██║██╔══╝  ██║           ║
    ║       ██║   ██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗      ║
    ║       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝      ║
    ║                                                              ║
    ║         Сервис подбора туристических маршрутов               ║
    ║              по Республике Тыва (Тува)                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(logo)


def print_header(title):
    print("─" * 70)
    print(f"  {title}")
    print("─" * 70)


def animate_text(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def get_user_preferences():
    preferences = {}

    print_header("ПЛАНИРОВАНИЕ МАРШРУТА")

    while True:
        try:
            days = int(input("\n📅 На сколько дней планируете путешествие? (1-14): "))
            if 1 <= days <= 14:
                preferences['days'] = days
                break
            else:
                print("❌ Пожалуйста, введите число от 1 до 14")
        except ValueError:
            print("❌ Пожалуйста, введите целое число")

    while True:
        try:
            budget = int(input("\n💰 Какой у вас общий бюджет на поездку? (руб): "))
            if budget > 0:
                preferences['budget'] = budget
                break
            else:
                print("❌ Бюджет должен быть положительным числом")
        except ValueError:
            print("❌ Пожалуйста, введите число")

    db = get_db()
    categories = db.get_all_categories()

    print("\n🎯 Выберите интересующие вас категории:")
    for i, category in enumerate(categories, 1):
        print(f"   {i}. {category}")
    print(f"   {len(categories) + 1}. Все категории")

    selected_categories = []
    while True:
        choices = input(f"\nВведите номера через запятую (1-{len(categories) + 1}): ")
        choice_nums = []

        for choice in choices.split(','):
            choice = choice.strip()
            if choice.isdigit():
                num = int(choice)
                if 1 <= num <= len(categories) + 1:
                    choice_nums.append(num)

        if choice_nums:
            if len(categories) + 1 in choice_nums:
                selected_categories = categories.copy()
            else:
                selected_categories = [categories[num - 1] for num in choice_nums if 1 <= num <= len(categories)]
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

    preferences['categories'] = selected_categories

    print("\n🌤️  Выберите сезон поездки:")
    seasons = ['лето', 'осень', 'зима', 'весна', 'круглый год']
    for i, season in enumerate(seasons, 1):
        print(f"   {i}. {season}")

    while True:
        try:
            season_choice = int(input("Ваш выбор (1-5): "))
            if 1 <= season_choice <= 5:
                preferences['season'] = seasons[season_choice - 1]
                break
        except ValueError:
            print("❌ Пожалуйста, введите число от 1 до 5")

    print("\n🏨 Выберите уровень комфорта:")
    comfort_levels = ['эконом', 'средний', 'комфорт']
    for i, level in enumerate(comfort_levels, 1):
        print(f"   {i}. {level}")

    while True:
        try:
            comfort_choice = int(input("Ваш выбор (1-3): "))
            if 1 <= comfort_choice <= 3:
                preferences['comfort_level'] = comfort_levels[comfort_choice - 1]
                break
        except ValueError:
            print("❌ Пожалуйста, введите число от 1 до 3")

    print("\n👥 С кем вы путешествуете?")
    traveler_types = ["Один/одна", "Пара", "Семья с детьми",
                     "Компания друзей", "Групповой тур"]

    for i, t_type in enumerate(traveler_types, 1):
        print(f"   {i}. {t_type}")

    while True:
        try:
            choice = int(input(f"\nВаш выбор (1-{len(traveler_types)}): "))
            if 1 <= choice <= len(traveler_types):
                preferences['traveler_type'] = traveler_types[choice - 1]
                break
        except ValueError:
            print(f"❌ Пожалуйста, введите число от 1 до {len(traveler_types)}")

    print("\n🚗 Какой транспорт предпочитаете?")
    transport_options = ["Личный автомобиль", "Общественный транспорт",
                        "Арендованный автомобиль", "Такси/трансферы", "Пешие прогулки"]

    for i, transport in enumerate(transport_options, 1):
        print(f"   {i}. {transport}")

    while True:
        try:
            choice = int(input(f"\nВаш выбор (1-{len(transport_options)}): "))
            if 1 <= choice <= len(transport_options):
                preferences['transport_type'] = transport_options[choice - 1]
                break
        except ValueError:
            print(f"❌ Пожалуйста, введите число от 1 до {len(transport_options)}")

    print("\n⚡ Уровень активности:")
    activity_levels = ["Спокойный", "Умеренный", "Активный", "Экстремальный"]

    for i, level in enumerate(activity_levels, 1):
        print(f"   {i}. {level}")

    while True:
        try:
            choice = int(input(f"\nВаш выбор (1-{len(activity_levels)}): "))
            if 1 <= choice <= len(activity_levels):
                preferences['activity_level'] = activity_levels[choice - 1]
                break
        except ValueError:
            print(f"❌ Пожалуйста, введите число от 1 до {len(activity_levels)}")

    print("\n🍽️ Предпочтения в питании:")
    food_options = ["Экономный вариант", "Кафе и рестораны",
                   "Гастрономический тур", "Национальная кухня", "Без предпочтений"]

    for i, food in enumerate(food_options, 1):
        print(f"   {i}. {food}")

    while True:
        try:
            choice = int(input(f"\nВаш выбор (1-{len(food_options)}): "))
            if 1 <= choice <= len(food_options):
                preferences['food_preference'] = food_options[choice - 1]
                break
        except ValueError:
            print(f"❌ Пожалуйста, введите число от 1 до {len(food_options)}")

    print("\n📧 Хотите сохранить маршрут? (опционально)")
    save_choice = input("Введите email для сохранения или нажмите Enter чтобы пропустить: ").strip()
    if save_choice:
        preferences['user_email'] = save_choice

    print("\n✅ Все предпочтения сохранены!")
    print("Нажмите Enter для генерации маршрута...")
    return preferences


def display_route(route, stats, preferences, recommendations=None):
    clear_screen()
    print_logo()

    print_header("ВАШ ПЕРСОНАЛИЗИРОВАННЫЙ МАРШРУТ")

    print(f"\n📋 ВАШИ ПАРАМЕТРЫ:")
    print(f"   • Дней в путешествии: {preferences.get('days', 'не указано')}")
    print(f"   • Общий бюджет: {preferences.get('budget', 0):,} руб")
    print(f"   • Сезон: {preferences.get('season', 'не указан').capitalize()}")
    print(f"   • Уровень комфорта: {preferences.get('comfort_level', 'средний')}")
    print(f"   • Тип путешественника: {preferences.get('traveler_type', 'не указано')}")
    print(f"   • Транспорт: {preferences.get('transport_type', 'не указано')}")
    print(f"   • Уровень активности: {preferences.get('activity_level', 'не указано')}")
    print(f"   • Питание: {preferences.get('food_preference', 'не указано')}")
    print(f"   • Категории: {', '.join(preferences.get('categories', []))}")

    print(f"\n📊 СТАТИСТИКА МАРШРУТА:")
    print(f"   • Дней запланировано: {stats['days']}")
    print(f"   • Общая стоимость посещений: {stats['total_cost']:,} руб")
    print(f"   • Общее время на посещения: {stats['total_hours']} часов")
    print(f"   • Количество мест: {stats['total_places']}")
    print(f"   • Средняя стоимость в день: {stats['avg_cost_per_day']:.0f} руб")
    if stats.get('places_by_category'):
        print(f"\n🏷️  РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ:")
        for category, count in stats['places_by_category'].items():
            print(f"   • {category}: {count} мест(а)")

    food_preference = preferences.get('food_preference', 'Кафе и рестораны')
    food_budget_per_day = 500

    if 'Экономный вариант' in food_preference:
        food_budget_per_day = 500
    elif 'Кафе и рестораны' in food_preference:
        food_budget_per_day = 1000
    elif 'Гастрономический тур' in food_preference:
        food_budget_per_day = 2000
    elif 'Национальная кухня' in food_preference:
        food_budget_per_day = 1500

    total_food_budget = food_budget_per_day * stats['days']
    print(f"   • Рекомендовано на питание: {total_food_budget:,} руб")

    print(f"\n📅 ДЕТАЛЬНЫЙ ПЛАН ПО ДНЯМ:")
    print("─" * 70)

    for day_num, day_places in enumerate(route, 1):
        day_cost = sum(place['cost'] for place in day_places)
        day_hours = sum(place.get('time_required', 2) for place in day_places)

        print(f"\nДЕНЬ {day_num}:")
        print(f"  ⏰ Всего времени: {day_hours} часов")
        print(f"  💰 Стоимость дня: {day_cost:,} руб")
        print(f"  🍽️  Питание: {food_budget_per_day:,} руб")
        print(f"  📍 Мест для посещения: {len(day_places)}")
        print("  " + "─" * 50)

        for i, place in enumerate(day_places, 1):
            print(f"  {i}. {place['name']}")
            print(f"     🏷️  Категория: {place['category']}")
            print(f"     📍 Местоположение: {place['city']}")
            print(f"     ⏱️  Время: {place.get('time_required', 2)} часа")
            print(f"     💰 Стоимость: {place['cost']:,} руб")
            print(f"     🌤️  Сезон: {place.get('season', 'круглый год')}")

            desc = place.get('description', '')
            if len(desc) > 80:
                desc = desc[:80] + "..."
            if desc:
                print(f"     📝 {desc}")
            print()

    if recommendations:
        print_header("ПЕРСОНАЛЬНЫЕ РЕКОМЕНДАЦИИ")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")

    print_header("АНАЛИЗ БЮДЖЕТА")
    total_budget = preferences.get('budget', 0)
    total_costs = stats['total_cost'] + total_food_budget
    remaining = total_budget - total_costs

    print(f"📊 ИТОГОВЫЙ РАСЧЁТ:")
    print(f"   • Стоимость посещений: {stats['total_cost']:,} руб")
    print(f"   • Питание: {total_food_budget:,} руб")
    print(f"   • Всего расходов: {total_costs:,} руб")
    print(f"   • Общий бюджет: {total_budget:,} руб")
    print(f"   • Остаток: {remaining:,} руб")

    if remaining > 0:
        print(f"\n✅ Отлично! У вас остаётся {remaining:,} руб на:")
        print(f"   • Транспорт и перемещения")
        print(f"   • Проживание")
        print(f"   • Сувениры и непредвиденные расходы")
    elif remaining == 0:
        print(f"\n⚠️  Бюджет полностью распределён.")
        print(f"   Учтите дополнительные расходы на транспорт и проживание.")
    else:
        print(f"\n⚠️  Внимание: превышение бюджета на {abs(remaining):,} руб.")
        print(f"   Рекомендуем пересмотреть маршрут или увеличить бюджет.")

    print_header("СОВЕТЫ ДЛЯ ВАШЕГО ТИПА ПУТЕШЕСТВЕННИКА")

    traveler_type = preferences.get('traveler_type', '')
    transport_type = preferences.get('transport_type', '')
    activity_level = preferences.get('activity_level', '')

    if 'Семья с детьми' in traveler_type:
        print("👨‍👩‍👧‍👦 Для семьи с детьми:")
        print("   • Проверьте наличие детских комнат в местах посещения")
        print("   • Планируйте больше времени на переезды и отдых")
        print("   • Возьмите воду, перекусы и аптечку")
        print("   • Рассмотрите места с игровыми площадками")

    if 'Пара' in traveler_type:
        print("💑 Для пары:")
        print("   • Забронируйте уютное жильё заранее")
        print("   • Посетите романтические места для фото")
        print("   • Попробуйте ужин в ресторане с национальной кухней")

    if 'Общественный транспорт' in transport_type:
        print("🚌 При использовании общественного транспорта:")
        print("   • Уточняйте расписание заранее")
        print("   • Рассмотрите места в радиусе 50 км от Кызыла")
        print("   • Имейте запас наличных для такси")
        print("   • Загрузите офлайн-карты")

    if 'Экстремальный' in activity_level:
        print("⚠️  Для экстремального отдыха:")
        print("   • Проверьте свою экипировку")
        print("   • Убедитесь в наличии гидов")
        print("   • Учитывайте погодные условия")
        print("   • Сообщите о своих планах близким")

    if 'Гастрономический тур' in preferences.get('food_preference', ''):
        print("🍽️  Для гастрономического тура:")
        print("   • Бронируйте столики в ресторанах заранее")
        print("   • Попробуйте местные деликатесы: боорзаки, хан")
        print("   • Посетите местные рынки")
        print("   • Участвуйте в мастер-классах по кулинарии")

    print(f"\n✨ Приятного путешествия по удивительной Республике Тыва!")


def save_route_to_db(route, stats, preferences):
    if 'user_email' not in preferences or not preferences['user_email']:
        return None

    db = get_db()

    place_ids = []
    for day_places in route:
        for place in day_places:
            place_ids.append(place['id'])

    route_id = db.save_route(
        preferences['user_email'],
        place_ids,
        stats['days'],
        stats['total_cost'],
        preferences
    )

    return route_id


def show_sample_routes():
    clear_screen()
    print_logo()
    print_header("ПРИМЕРЫ ГОТОВЫХ МАРШРУТОВ")

    generator = RouteGenerator()
    samples = generator.generate_sample_routes()

    print("Вот несколько примеров маршрутов, которые можно создать:\n")

    for i, sample in enumerate(samples, 1):
        print(f"{i}. {sample['name']}")
        print(f"   • Дней: {sample['preferences']['days']}")
        print(f"   • Бюджет: {sample['preferences']['budget']:,} руб")
        print(f"   • Тип: {sample['preferences'].get('traveler_type', 'не указан')}")
        print(f"   • Транспорт: {sample['preferences'].get('transport_type', 'не указан')}")
        print(f"   • Активность: {sample['preferences'].get('activity_level', 'не указан')}")
        print(f"   • Категории: {', '.join(sample['preferences']['categories'])}")
        print(f"   • Стоимость: {sample['stats']['total_cost']} руб")
        print(f"   • Мест: {sample['stats']['total_places']}")
        print()
        print("\nНажмите Enter для возврата в меню...")


def export_route_menu(route, stats, preferences):
    exporter = ExportManager()
    formats = exporter.get_export_formats()

    while True:
        clear_screen()
        print_logo()
        print_header("ЭКСПОРТ МАРШРУТА")

        print("Доступные форматы экспорта:\n")
        for i, fmt in enumerate(formats, 1):
            print(f"{i}. {fmt['name']}")
            print(f"   {fmt['description']}\n")

        print(f"{len(formats) + 1}. Вернуться в главное меню")

        try:
            choice = int(input(f"\nВыберите формат (1-{len(formats) + 1}): "))

            if 1 <= choice <= len(formats):
                format_id = formats[choice - 1]['id']

                print(f"\n⚙️  Экспортируем в {formats[choice - 1]['name']}...")

                if format_id == 'txt':
                    filepath = exporter.export_to_txt(
                        route, stats, preferences,
                        preferences.get('user_email')
                    )
                elif format_id == 'html':
                    filepath = exporter.export_to_html(route, stats, preferences)
                else:
                    print("❌ Неизвестный формат")
                    continue

                print(f"\n✅ Маршрут успешно экспортирован!")
                print(f"📁 Файл: {filepath}")

                if format_id == 'html':
                    open_file = input("\nОткрыть файл в браузере? (да/нет): ").strip().lower()
                    if open_file == 'да':
                        import webbrowser
                        webbrowser.open(f'file://{os.path.abspath(filepath)}')

                print("\nНажмите Enter для продолжения...")
                return True

            elif choice == len(formats) + 1:
                return False
            else:
                print("❌ Неверный выбор")
                print("\nНажмите Enter для продолжения...")

        except ValueError:
            print("❌ Пожалуйста, введите число")
            print("\nНажмите Enter для продолжения...")


def main():
    db = get_db()
    generator = RouteGenerator()

    while True:
        clear_screen()
        print_logo()

        print_header("ГЛАВНОЕ МЕНЮ")
        print("1. 🗺️ Создать новый маршрут")
        print("2. 📋 Посмотреть примеры маршрутов")
        print("3. ⚙️ Административная панель")
        print("4. 📊 Статистика системы")
        print("5. 🚪 Выйти из программы")
        print()

        try:
            choice = int(input("Выберите действие (1-5): "))

            if choice == 1:
                preferences = get_user_preferences()

                print("\n⚙️  Генерируем оптимальный маршрут...")
                print("Это может занять несколько секунд...")

                route = generator.generate_route(preferences)

                if not route:
                    print("❌ Не удалось сгенерировать маршрут с указанными параметрами.")
                    print("   Попробуйте изменить бюджет или категории.")
                    print("\nНажмите Enter для продолжения...")
                    continue

                stats = generator.calculate_route_stats(route)
                recommendations = generator.get_recommendations(route, preferences)

                display_route(route, stats, preferences, recommendations)

                if 'user_email' in preferences:
                    route_id = save_route_to_db(route, stats, preferences)
                    if route_id:
                        print(f"\n✅ Маршрут сохранён в базе данных (ID: {route_id})")

                while True:
                    print("\n" + "─" * 60)
                    print("ДОПОЛНИТЕЛЬНЫЕ ДЕЙСТВИЯ:")
                    print("1. 📤 Экспортировать маршрут в файл")
                    print("2. 🔄 Создать новый маршрут")
                    print("3. 🏠 Вернуться в главное меню")

                    try:
                        action = int(input("\nВыберите действие (1-3): "))

                        if action == 1:
                            export_route_menu(route, stats, preferences)
                        elif action == 2:
                            break
                        elif action == 3:
                            break 
                        else:
                            print("❌ Неверный выбор")
                    except ValueError:
                        print("❌ Пожалуйста, введите число")

            elif choice == 2:
                show_sample_routes()
                
            elif choice == 3:
                clear_screen()
                print("Для входа в админ-панель требуется пароль.")
                print("Для демонстрации используйте пароль: admin123")
                print("\nНажмите Enter чтобы продолжить...")
                import subprocess
                subprocess.run([sys.executable, "admin.py"])

            elif choice == 4:
                clear_screen()
                print_logo()
                print_header("СТАТИСТИКА СИСТЕМЫ")

                stats = db.get_system_stats()

                print(f"📊 ОБЩАЯ СТАТИСТИКА:")
                print(f"   • Туристических мест: {stats['total_places']}")
                print(f"   • Пользователей: {stats['total_users']}")
                print(f"   • Сгенерированных маршрутов: {stats['total_routes']}")
                print(f"   • Общая стоимость маршрутов: {stats['total_money_calculated']:,} руб")

                categories = db.get_all_categories()
                print(f"\n🏷️  КАТЕГОРИИ ({len(categories)}):")
                for category in categories:
                    places = db.get_places_by_category(category)
                    print(f"   • {category}: {len(places)} мест")
                print("\n\nНажмите Enter для возврата...")

            elif choice == 5:
                print("\n👋 Спасибо за использование TyvaTravelPlanner!")
                print("   Приятного путешествия по Республике Тыва!")
                print()
                db.close()
                time.sleep(2)
                break

            else:
                print("❌ Неверный выбор. Попробуйте снова.")
                print("\nНажмите Enter для продолжения...")

        except ValueError:
            print("❌ Пожалуйста, введите число от 1 до 6")
            print("\nНажмите Enter для продолжения...")
        except (KeyboardInterrupt, EOFError, RuntimeError):
            print("\n\n👋 Программа завершена пользователем.")
            db.close()
            break
        except Exception as e:
            print(f"\n❌ Произошла ошибка: {e}")
            print("Попробуйте снова или перезапустите программу.")
            print("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    if not os.path.exists('exports'):
        os.makedirs('exports')

    try:
        main()
    except (KeyboardInterrupt, EOFError, RuntimeError):
        print("\n\n👋 До свидания!")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("Пожалуйста, перезапустите программу.")
        print("\nНажмите Enter для выхода...")