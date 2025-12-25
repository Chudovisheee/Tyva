import os
import json
from datetime import datetime
from database import get_db


class ExportManager:
    def __init__(self, export_dir='exports'):
        self.export_dir = export_dir
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

    def export_to_txt(self, route, stats, preferences, user_email=None):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        traveler_type = preferences.get('traveler_type', 'общий')
        days = preferences.get('days', 1)
        filename = f"маршрут_Тыва_{traveler_type.replace(' ', '_')}_{days}дней_{timestamp}.txt"
        filepath = os.path.join(self.export_dir, filename)

        db = get_db()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(" " * 25 + "🌄 ТУРИСТИЧЕСКИЙ МАРШРУТ\n")
            f.write(" " * 20 + "РЕСПУБЛИКА ТЫВА (ТУВА)\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"📅 Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write(f"📊 Версия маршрута: 2.0 (с расширенными параметрами)\n")

            if user_email:
                f.write(f"👤 Для пользователя: {user_email}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("🎯 ПАРАМЕТРЫ ПУТЕШЕСТВИЯ:\n")
            f.write("=" * 80 + "\n\n")

            f.write("📋 ОСНОВНЫЕ ПАРАМЕТРЫ:\n")
            f.write("-" * 40 + "\n")
            f.write(f"• Дней в поездке: {preferences.get('days', 'не указано')}\n")
            f.write(f"• Бюджет: {preferences.get('budget', 'не указан'):,} руб\n")
            f.write(f"• Сезон: {preferences.get('season', 'не указан').capitalize()}\n")
            f.write(f"• Уровень комфорта: {preferences.get('comfort_level', 'средний')}\n")

            f.write("\n👥 ПЕРСОНАЛИЗАЦИЯ:\n")
            f.write("-" * 40 + "\n")
            f.write(f"• Тип путешественника: {preferences.get('traveler_type', 'не указано')}\n")
            f.write(f"• Транспорт: {preferences.get('transport_type', 'не указано')}\n")
            f.write(f"• Уровень активности: {preferences.get('activity_level', 'не указано')}\n")
            f.write(f"• Питание: {preferences.get('food_preference', 'не указано')}\n")

            f.write("\n🏷️ ИНТЕРЕСЫ:\n")
            f.write("-" * 40 + "\n")
            categories = preferences.get('categories', [])
            if categories:
                f.write(f"• Категории: {', '.join(categories)}\n")
            else:
                f.write("• Категории: не указаны\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("📊 СТАТИСТИКА МАРШРУТА:\n")
            f.write("=" * 80 + "\n\n")

            f.write("💰 ФИНАНСОВАЯ СТАТИСТИКА:\n")
            f.write("-" * 40 + "\n")
            f.write(f"• Общая стоимость посещений: {stats['total_cost']:,} руб\n")
            f.write(f"• Общее время на посещения: {stats['total_hours']} часов\n")
            f.write(f"• Количество мест: {stats['total_places']}\n")
            f.write(f"• Дней в маршруте: {stats['days']}\n")
            f.write(f"• Средняя стоимость в день: {stats['avg_cost_per_day']:.0f} руб\n")

            food_preference = preferences.get('food_preference', 'Кафе и рестораны')
            food_budget_per_day = self._calculate_food_budget(food_preference)
            total_food_budget = food_budget_per_day * stats['days']

            f.write(f"\n🍽️  РАСЧЁТ НА ПИТАНИЕ:\n")
            f.write("-" * 40 + "\n")
            f.write(f"• Предпочтения: {food_preference}\n")
            f.write(f"• Бюджет в день: {food_budget_per_day:,} руб\n")
            f.write(f"• Всего на питание: {total_food_budget:,} руб\n")

            total_budget = preferences.get('budget', 0)
            total_expenses = stats['total_cost'] + total_food_budget
            remaining = total_budget - total_expenses

            f.write(f"\n💎 ИТОГОВЫЙ ФИНАНСОВЫЙ ОТЧЁТ:\n")
            f.write("-" * 40 + "\n")
            f.write(f"• Посещения: {stats['total_cost']:,} руб\n")
            f.write(f"• Питание: {total_food_budget:,} руб\n")
            f.write(f"• Всего расходов: {total_expenses:,} руб\n")
            f.write(f"• Общий бюджет: {total_budget:,} руб\n")
            f.write(f"• Остаток: {remaining:,} руб\n")

            if remaining > 0:
                f.write(f"✅ Отлично! У вас остаётся {remaining:,} руб на другие расходы.\n")
            elif remaining == 0:
                f.write(f"⚠️  Бюджет полностью распределён. Учтите дополнительные расходы.\n")
            else:
                f.write(f"⚠️  Внимание: превышение бюджета на {abs(remaining):,} руб.\n")

            if stats.get('places_by_category'):
                f.write(f"\n🏷️  РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ:\n")
                f.write("-" * 40 + "\n")
                for category, count in stats['places_by_category'].items():
                    percentage = (count / stats['total_places']) * 100
                    f.write(f"  {category}: {count} мест ({percentage:.0f}%)\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("📅 ДЕТАЛЬНЫЙ ПЛАН ПО ДНЯМ:\n")
            f.write("=" * 80 + "\n")

            for day_num, day_places in enumerate(route, 1):
                day_cost = sum(place['cost'] for place in day_places)
                day_hours = sum(place.get('time_required', 2) for place in day_places)

                f.write(f"\n{'=' * 60}\n")
                f.write(f"ДЕНЬ {day_num}:\n")
                f.write(f"{'=' * 60}\n")
                f.write(f"💰 Стоимость дня: {day_cost:,} руб\n")
                f.write(f"⏱️  Общее время: {day_hours} часов\n")
                f.write(f"📍 Мест для посещения: {len(day_places)}\n")
                f.write(f"🍽️  Питание: {food_budget_per_day:,} руб\n")
                f.write("-" * 60 + "\n")

                for i, place in enumerate(day_places, 1):
                    f.write(f"\n{i}. {place['name'].upper()}\n")
                    f.write(f"   🏷️  Категория: {place['category']}\n")
                    f.write(f"   📍 Местоположение: {place['city']}\n")
                    f.write(f"   ⏱️  Время на посещение: {place.get('time_required', 2)} часа\n")
                    f.write(f"   💰 Стоимость: {place['cost']:,} руб\n")
                    f.write(f"   🌤️  Сезон: {place.get('season', 'круглый год')}\n")

                    desc = place.get('description', 'Описание отсутствует')
                    f.write(f"   📝 Описание: {self._wrap_text(desc, width=70, indent=7)}\n")

                f.write(f"\n💡 СОВЕТЫ НА ДЕНЬ {day_num}:\n")
                f.write("-" * 40 + "\n")
                f.write(f"• Начните день рано, чтобы успеть всё посмотреть\n")
                f.write(f"• Заранее проверьте время работы объектов\n")
                f.write(f"• Возьмите воду и перекусы с собой\n")
                if day_hours > 6:
                    f.write(f"• Сегодня насыщенный день - планируйте время на отдых\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("💡 ПЕРСОНАЛЬНЫЕ РЕКОМЕНДАЦИИ:\n")
            f.write("=" * 80 + "\n\n")

            traveler_type = preferences.get('traveler_type', '')
            transport_type = preferences.get('transport_type', '')
            activity_level = preferences.get('activity_level', '')
            food_preference = preferences.get('food_preference', '')

            f.write("👥 ДЛЯ ВАШЕГО ТИПА ПУТЕШЕСТВЕННИКА:\n")
            f.write("-" * 40 + "\n")

            if 'Семья с детьми' in traveler_type:
                f.write("• Проверьте наличие детских комнат в местах посещения\n")
                f.write("• Планируйте больше времени на переезды и отдых\n")
                f.write("• Возьмите с собой воду, перекусы и аптечку\n")
                f.write("• Рассмотрите места с игровыми площадками\n")
            elif 'Пара' in traveler_type:
                f.write("• Забронируйте уютное жильё заранее\n")
                f.write("• Посетите романтические места для фото\n")
                f.write("• Попробуйте ужин в ресторане с национальной кухней\n")
                f.write("• Запланируйте время для отдыха вдвоём\n")
            elif 'Компания друзей' in traveler_type:
                f.write("• Разделите обязанности между участниками\n")
                f.write("• Рассмотрите групповые экскурсии и активности\n")
                f.write("• Забронируйте жильё с общей зоной\n")
                f.write("• Запланируйте совместные ужины\n")
            else:
                f.write("• Путешествуйте в своём темпе\n")
                f.write("• Не бойтесь менять планы по ходу поездки\n")
                f.write("• Знакомьтесь с местными жителями\n")

            f.write(f"\n🚗 РЕКОМЕНДАЦИИ ПО ТРАНСПОРТУ ({transport_type}):\n")
            f.write("-" * 40 + "\n")

            if 'Общественный транспорт' in transport_type:
                f.write("• Уточняйте расписание транспорта заранее\n")
                f.write("• Рассмотрите места в радиусе 50 км от Кызыла\n")
                f.write("• Имейте запас наличных для такси\n")
                f.write("• Загрузите офлайн-карты для навигации\n")
                f.write("• Учитывайте время на ожидание транспорта\n")
            elif 'Личный автомобиль' in transport_type or 'Арендованный автомобиль' in transport_type:
                f.write("• Проверьте состояние автомобиля перед поездкой\n")
                f.write("• Заправляйтесь в крупных населённых пунктах\n")
                f.write("• Имейте запасное колесо и инструменты\n")
                f.write("• Учитывайте качество дорог в отдалённых районах\n")
                f.write("• Паркуйтесь только в разрешённых местах\n")
            elif 'Пешие прогулки' in transport_type:
                f.write("• Выберите удобную обувь\n")
                f.write("• Учитывайте погодные условия\n")
                f.write("• Берите с собой воду и карту\n")
                f.write("• Планируйте маршруты с учётом физической подготовки\n")

            f.write(f"\n⚡ РЕКОМЕНДАЦИИ ПО АКТИВНОСТИ ({activity_level}):\n")
            f.write("-" * 40 + "\n")

            if 'Экстремальный' in activity_level:
                f.write("• Проверьте свою экипировку и снаряжение\n")
                f.write("• Убедитесь в наличии опытных гидов\n")
                f.write("• Учитывайте погодные условия\n")
                f.write("• Сообщите о своих планах близким\n")
                f.write("• Имейте план на случай непредвиденных ситуаций\n")
            elif 'Активный' in activity_level:
                f.write("• Планируйте время на восстановление\n")
                f.write("• Берите с собой спортивную одежду\n")
                f.write("• Пейте достаточно воды\n")
                f.write("• Слушайте своё тело и не перегружайтесь\n")
            elif 'Спокойный' in activity_level:
                f.write("• Запланируйте время для отдыха между посещениями\n")
                f.write("• Выбирайте комфортный темп\n")
                f.write("• Рассмотрите места для релаксации\n")
                f.write("• Не спешите - наслаждайтесь моментом\n")

            f.write(f"\n🍽️  РЕКОМЕНДАЦИИ ПО ПИТАНИЮ ({food_preference}):\n")
            f.write("-" * 40 + "\n")

            if 'Гастрономический тур' in food_preference:
                f.write("• Бронируйте столики в ресторанах заранее\n")
                f.write("• Попробуйте местные деликатесы: боорзаки, хан, тувинский чай\n")
                f.write("• Посетите местные рынки для покупки традиционных продуктов\n")
                f.write("• Участвуйте в мастер-классах по кулинарии\n")
                f.write("• Ведите гастрономический дневник\n")
            elif 'Национальная кухня' in food_preference:
                f.write("• Посетите юрточные кафе и местные столовые\n")
                f.write("• Попробуйте блюда на открытом огне\n")
                f.write("• Спросите у местных жителей о лучших местах\n")
                f.write("• Участвуйте в дегустациях местных продуктов\n")
            elif 'Экономный вариант' in food_preference:
                f.write("• Покупайте продукты в местных магазинах\n")
                f.write("• Готовьте сами, если есть возможность\n")
                f.write("• Ищите столовые с местной кухней\n")
                f.write("• Берите с собой перекусы в дорогу\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("🌟 ОБЩИЕ СОВЕТЫ ДЛЯ ПУТЕШЕСТВИЯ ПО ТЫВЕ:\n")
            f.write("=" * 80 + "\n\n")

            general_tips = [
                "Всегда имейте с собой наличные деньги - не везде есть терминалы",
                "Бронируйте жильё заранее, особенно в высокий сезон (июль-август)",
                "Сохраните офлайн-карты местности для навигации",
                "Уважайте местные традиции, обычаи и священные места",
                "Изучите несколько фраз на тувинском языке - это расположит местных жителей",
                "Учитывайте разницу во времени с Москвой (+4 часа)",
                "Берите с собой паспорт - некоторые объекты требуют документы",
                "Проверяйте погоду перед выездом - в горах она меняется быстро",
                "Имейте аптечку с базовыми лекарствами",
                "Сохраните контакты экстренных служб"
            ]

            for i, tip in enumerate(general_tips, 1):
                f.write(f"{i}. {tip}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("🚨 ЭКСТРЕННЫЕ КОНТАКТЫ:\n")
            f.write("=" * 80 + "\n\n")

            emergency_contacts = [
                ("Скорая помощь", "103 или 112"),
                ("Полиция", "102 или 112"),
                ("МЧС", "101 или 112"),
                ("Единая служба спасения", "112"),
                ("Туристическая информация Кызыл", "+7 (394-22) 2-22-22"),
                ("Такси Кызыл", "+7 (394-22) 3-33-33"),
                ("Больница скорой помощи Кызыл", "+7 (394-22) 5-55-55"),
                ("Аптека 24 часа", "+7 (394-22) 6-66-66")
            ]

            for service, number in emergency_contacts:
                f.write(f"• {service}: {number}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("✨ ПРИЯТНОГО ПУТЕШЕСТВИЯ ПО РЕСПУБЛИКЕ ТЫВА!\n")
            f.write("=" * 80 + "\n")
            f.write(f"\nФайл создан автоматически сервисом TyvaTravelPlanner Pro v2.0\n")
            f.write(f"Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write(f"Контактная информация: tyva-travel@example.com\n")
            f.write(f"Официальный сайт: www.tyva-travel-planner.ru\n")

        print(f"[Экспорт] Маршрут сохранён в файл: {filepath}")
        return filepath

    def export_to_html(self, route, stats, preferences):
        """Экспорт маршрута в HTML-файл с новыми параметрами"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"маршрут_Тыва_{timestamp}.html"
        filepath = os.path.join(self.export_dir, filename)

        # Рассчитываем бюджет на питание
        food_preference = preferences.get('food_preference', 'Кафе и рестораны')
        food_budget_per_day = self._calculate_food_budget(food_preference)
        total_food_budget = food_budget_per_day * stats['days']
        total_expenses = stats['total_cost'] + total_food_budget
        remaining = preferences.get('budget', 0) - total_expenses

        html_content = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Маршрут по Республике Тыва - TyvaTravelPlanner Pro</title>
            <style>
                /* Основные стили */
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0;
                    padding: 0;
                    background-color: #f8f9fa;
                    color: #333;
                    line-height: 1.6;
                }}

                .container {{ 
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}

                /* Шапка */
                .header {{ 
                    background: linear-gradient(135deg, #2c3e50, #3498db);
                    color: white;
                    padding: 40px 20px;
                    text-align: center;
                    border-radius: 0 0 20px 20px;
                    margin-bottom: 40px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }}

                .header h1 {{ 
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: 300;
                }}

                .header .subtitle {{ 
                    margin-top: 10px;
                    font-size: 1.2em;
                    opacity: 0.9;
                }}

                /* Секции */
                .section {{ 
                    background: white;
                    margin-bottom: 30px;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    border-left: 5px solid #3498db;
                }}

                .section h2 {{ 
                    color: #2c3e50;
                    margin-top: 0;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #eee;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}

                /* Карточки */
                .card {{ 
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    border: 1px solid #e9ecef;
                }}

                .card h3 {{ 
                    color: #2c3e50;
                    margin-top: 0;
                }}

                /* Статистика в сетке */
                .stats-grid {{ 
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}

                .stat-item {{ 
                    background: linear-gradient(135deg, #3498db, #2c3e50);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                }}

                .stat-value {{ 
                    font-size: 2em;
                    font-weight: bold;
                    margin: 10px 0;
                }}

                .stat-label {{ 
                    font-size: 0.9em;
                    opacity: 0.9;
                }}

                /* Дни */
                .day {{ 
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 25px;
                    margin-bottom: 25px;
                    border-left: 4px solid #e74c3c;
                }}

                .day-header {{ 
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 1px solid #dee2e6;
                }}

                .day-title {{ 
                    font-size: 1.5em;
                    color: #2c3e50;
                    margin: 0;
                }}

                .day-stats {{ 
                    display: flex;
                    gap: 20px;
                    color: #6c757d;
                }}

                /* Места */
                .place {{ 
                    background: white;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 15px;
                    border: 1px solid #e9ecef;
                }}

                .place h4 {{ 
                    color: #2c3e50;
                    margin-top: 0;
                    margin-bottom: 10px;
                }}

                .place-meta {{ 
                    display: flex;
                    flex-wrap: wrap;
                    gap: 15px;
                    margin-bottom: 10px;
                    color: #6c757d;
                    font-size: 0.9em;
                }}

                /* Цветовые индикаторы */
                .budget-good {{ color: #27ae60; font-weight: bold; }}
                .budget-warning {{ color: #f39c12; font-weight: bold; }}
                .budget-danger {{ color: #e74c3c; font-weight: bold; }}

                /* Списки */
                .tips-list {{ 
                    list-style-type: none;
                    padding: 0;
                }}

                .tips-list li {{ 
                    padding: 10px 0;
                    padding-left: 30px;
                    position: relative;
                }}

                .tips-list li:before {{
                    content: "✓";
                    position: absolute;
                    left: 0;
                    color: #27ae60;
                    font-weight: bold;
                }}

                /* Подвал */
                .footer {{ 
                    text-align: center;
                    margin-top: 50px;
                    padding: 30px;
                    background: #2c3e50;
                    color: white;
                    border-radius: 15px 15px 0 0;
                }}

                /* Адаптивность */
                @media (max-width: 768px) {{
                    .stats-grid {{ grid-template-columns: 1fr; }}
                    .day-header {{ flex-direction: column; align-items: flex-start; gap: 10px; }}
                    .day-stats {{ flex-wrap: wrap; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <h1>🌄 Tyva Travel Planner Pro</h1>
                    <div class="subtitle">Персонализированный маршрут по Республике Тыва</div>
                    <div style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                        Создано: {datetime.now().strftime('%d.%m.%Y %H:%M')}
                    </div>
                </div>
            </div>

            <div class="container">
                <!-- Секция параметров -->
                <div class="section">
                    <h2>📋 Параметры путешествия</h2>
                    <div class="stats-grid">
                        <div class="card">
                            <h3>Основные</h3>
                            <p><strong>Дней:</strong> {preferences.get('days', 'не указано')}</p>
                            <p><strong>Бюджет:</strong> {preferences.get('budget', 0):,} руб</p>
                            <p><strong>Сезон:</strong> {preferences.get('season', 'не указан').capitalize()}</p>
                            <p><strong>Комфорт:</strong> {preferences.get('comfort_level', 'средний')}</p>
                        </div>

                        <div class="card">
                            <h3>Персонализация</h3>
                            <p><strong>Тип:</strong> {preferences.get('traveler_type', 'не указано')}</p>
                            <p><strong>Транспорт:</strong> {preferences.get('transport_type', 'не указано')}</p>
                            <p><strong>Активность:</strong> {preferences.get('activity_level', 'не указано')}</p>
                            <p><strong>Питание:</strong> {preferences.get('food_preference', 'не указано')}</p>
                        </div>

                        <div class="card">
                            <h3>Категории интересов</h3>
                            <p>{', '.join(preferences.get('categories', ['не указаны']))}</p>
                        </div>
                    </div>
                </div>

                <!-- Секция статистики -->
                <div class="section">
                    <h2>📊 Статистика маршрута</h2>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-value">{stats['days']}</div>
                            <div class="stat-label">Дней</div>
                        </div>

                        <div class="stat-item">
                            <div class="stat-value">{stats['total_places']}</div>
                            <div class="stat-label">Мест</div>
                        </div>

                        <div class="stat-item">
                            <div class="stat-value">{stats['total_hours']} ч</div>
                            <div class="stat-label">Время</div>
                        </div>

                        <div class="stat-item">
                            <div class="stat-value">{stats['total_cost']:,} ₽</div>
                            <div class="stat-label">Стоимость</div>
                        </div>
                    </div>

                    <div class="card">
                        <h3>Финансовый отчёт</h3>
                        <p><strong>Посещения:</strong> {stats['total_cost']:,} руб</p>
                        <p><strong>Питание ({food_preference}):</strong> {total_food_budget:,} руб</p>
                        <p><strong>Всего расходов:</strong> {total_expenses:,} руб</p>
                        <p><strong>Общий бюджет:</strong> {preferences.get('budget', 0):,} руб</p>
                        <p><strong>Остаток:</strong> 
                            <span class="{'budget-good' if remaining > 0 else 'budget-danger'}">
                                {remaining:,} руб
                            </span>
                        </p>
                    </div>
                </div>

                <!-- Секция плана по дням -->
                <div class="section">
                    <h2>📅 План по дням</h2>
        """

        # Генерация дней
        for day_num, day_places in enumerate(route, 1):
            day_cost = sum(place['cost'] for place in day_places)
            day_hours = sum(place.get('time_required', 2) for place in day_places)

            html_content += f"""
                    <div class="day">
                        <div class="day-header">
                            <h3 class="day-title">День {day_num}</h3>
                            <div class="day-stats">
                                <span>💰 {day_cost:,} руб</span>
                                <span>⏱️ {day_hours} часов</span>
                                <span>📍 {len(day_places)} мест</span>
                                <span>🍽️ {food_budget_per_day:,} руб</span>
                            </div>
                        </div>
            """

            for place in day_places:
                html_content += f"""
                        <div class="place">
                            <h4>{place['name']}</h4>
                            <div class="place-meta">
                                <span>🏷️ {place['category']}</span>
                                <span>📍 {place['city']}</span>
                                <span>⏱️ {place.get('time_required', 2)} часа</span>
                                <span>💰 {place['cost']:,} руб</span>
                            </div>
                            <p>{place.get('description', 'Описание отсутствует')}</p>
                        </div>
                """

            html_content += """
                    </div>
            """

        html_content += f"""
                </div>

                <!-- Секция рекомендаций -->
                <div class="section">
                    <h2>💡 Персональные рекомендации</h2>
                    <div class="card">
                        <h3>Для {preferences.get('traveler_type', 'вашего типа')} путешественников</h3>
                        <ul class="tips-list">
        """

        # Генерация рекомендаций
        traveler_type = preferences.get('traveler_type', '')
        if 'Семья с детьми' in traveler_type:
            html_content += """
                            <li>Проверьте наличие детских комнат в местах посещения</li>
                            <li>Планируйте больше времени на переезды и отдых</li>
                            <li>Возьмите воду, перекусы и аптечку</li>
                            <li>Рассмотрите места с игровыми площадками</li>
            """
        elif 'Пара' in traveler_type:
            html_content += """
                            <li>Забронируйте уютное жильё заранее</li>
                            <li>Посетите романтические места для фото</li>
                            <li>Попробуйте ужин в ресторане с национальной кухней</li>
                            <li>Запланируйте время для отдыха вдвоём</li>
            """

        html_content += f"""
                        </ul>
                    </div>

                    <div class="card">
                        <h3>По транспорту ({preferences.get('transport_type', 'не указан')})</h3>
                        <ul class="tips-list">
        """

        transport_type = preferences.get('transport_type', '')
        if 'Общественный транспорт' in transport_type:
            html_content += """
                            <li>Уточняйте расписание транспорта заранее</li>
                            <li>Рассмотрите места в радиусе 50 км от Кызыла</li>
                            <li>Имейте запас наличных для такси</li>
                            <li>Загрузите офлайн-карты для навигации</li>
            """

        html_content += """
                        </ul>
                    </div>
                </div>

                <!-- Секция контактов -->
                <div class="section">
                    <h2>🚨 Экстренные контакты</h2>
                    <div class="stats-grid">
                        <div class="card">
                            <h3>Экстренные службы</h3>
                            <p>Скорая помощь: <strong>103 или 112</strong></p>
                            <p>Полиция: <strong>102 или 112</strong></p>
                            <p>МЧС: <strong>101 или 112</strong></p>
                            <p>Единая служба спасения: <strong>112</strong></p>
                        </div>

                        <div class="card">
                            <h3>Полезные контакты</h3>
                            <p>Туристическая информация: <strong>+7 (394-22) 2-22-22</strong></p>
                            <p>Такси Кызыл: <strong>+7 (394-22) 3-33-33</strong></p>
                            <p>Больница скорой помощи: <strong>+7 (394-22) 5-55-55</strong></p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="footer">
                <div class="container">
                    <p>✨ Приятного путешествия по удивительной Республике Тыва!</p>
                    <p>Создано с помощью TyvaTravelPlanner Pro v2.0</p>
                    <p>Контакт: tyva-travel@example.com | Сайт: www.tyva-travel-planner.ru</p>
                </div>
            </div>
        </body>
        </html>
        """

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[Экспорт] Маршрут сохранён в HTML: {filepath}")
        return filepath

    def get_export_formats(self):
        """Возвращает список доступных форматов экспорта с описанием"""
        return [
            {
                'id': 'txt',
                'name': '📄 Текстовый файл (.txt)',
                'description': 'Подробный текстовый отчёт с форматированием. Открывается в любом редакторе.',
                'features': ['Полные детали маршрута', 'Финансовый отчёт', 'Рекомендации', 'Контакты']
            },
            {
                'id': 'html',
                'name': '🌐 HTML страница (.html)',
                'description': 'Красочная веб-страница для просмотра в браузере. Можно распечатать.',
                'features': ['Красивый дизайн', 'Адаптивная вёрстка', 'Цветовые схемы', 'Готово к печати']
            }
        ]

    def _calculate_food_budget(self, food_preference):
        """Рассчитать бюджет на питание в день"""
        budgets = {
            'Экономный вариант': 500,
            'Кафе и рестораны': 1000,
            'Национальная кухня': 1500,
            'Гастрономический тур': 2000,
            'Без предпочтений': 800
        }
        return budgets.get(food_preference, 800)

    def _wrap_text(self, text, width=70, indent=0):
        """Переносить текст по словам с заданной шириной"""
        import textwrap
        wrapped = textwrap.fill(text, width=width)
        # Добавляем отступ к каждой строке
        lines = wrapped.split('\n')
        indent_str = ' ' * indent
        return '\n'.join([f"{indent_str}{line}" for line in lines])

    def _generate_recommendations(self, preferences):
        """Сгенерировать рекомендации на основе параметров"""
        recommendations = {
            'general': [
                'Всегда имейте с собой наличные деньги',
                'Бронируйте жильё заранее в высокий сезон',
                'Уважайте местные традиции и обычаи',
                'Сохраните офлайн-карты для навигации'
            ],
            'by_traveler_type': {},
            'by_transport': {},
            'by_activity': {},
            'by_food': {}
        }

        # Рекомендации по типу путешественника
        traveler_type = preferences.get('traveler_type', '')
        if 'Семья с детьми' in traveler_type:
            recommendations['by_traveler_type'] = [
                'Проверьте детскую инфраструктуру',
                'Планируйте больше времени на отдых',
                'Возьмите аптечку и перекусы',
                'Выбирайте места с игровыми площадками'
            ]
        elif 'Пара' in traveler_type:
            recommendations['by_traveler_type'] = [
                'Забронируйте уютное жильё',
                'Посетите романтические места',
                'Запланируйте ужин в ресторане',
                'Наслаждайтесь уединёнными местами'
            ]

        # Рекомендации по транспорту
        transport = preferences.get('transport_type', '')
        if 'Общественный транспорт' in transport:
            recommendations['by_transport'] = [
                'Уточняйте расписание заранее',
                'Рассматривайте ближние маршруты',
                'Имейте запас наличных для такси',
                'Учитывайте время на ожидание'
            ]

        return recommendations

    def export_all_formats(self, route, stats, preferences, user_email=None):
        """Экспорт во все доступные форматы сразу"""
        files = {}

        try:
            files['txt'] = self.export_to_txt(route, stats, preferences, user_email)
        except Exception as e:
            print(f"[Экспорт] Ошибка при экспорте в TXT: {e}")
            files['txt'] = None

        try:
            files['json'] = self.export_to_json(route, stats, preferences)
        except Exception as e:
            print(f"[Экспорт] Ошибка при экспорте в JSON: {e}")
            files['json'] = None

        try:
            files['html'] = self.export_to_html(route, stats, preferences)
        except Exception as e:
            print(f"[Экспорт] Ошибка при экспорте в HTML: {e}")
            files['html'] = None

        # Удаляем None значения
        files = {k: v for k, v in files.items() if v is not None}

        print(f"[Экспорт] Успешно экспортировано {len(files)} форматов")
        return files


# Удобная функция для быстрого экспорта
def export_route(route, stats, preferences, format='txt', user_email=None):
    """Быстрый экспорт маршрута в указанный формат"""
    exporter = ExportManager()

    if format == 'txt':
        return exporter.export_to_txt(route, stats, preferences, user_email)
    elif format == 'html':
        return exporter.export_to_html(route, stats, preferences)
    elif format == 'all':
        return exporter.export_all_formats(route, stats, preferences, user_email)
    else:
        raise ValueError(f"Неизвестный формат: {format}")