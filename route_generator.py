import random
import json
from database import get_db


class RouteGenerator:
    def __init__(self):
        self.db = get_db()

    def generate_route(self, preferences):
        print(f"[Генератор] Начало генерации маршрута с параметрами: {preferences}")

        traveler_type = preferences.get('traveler_type', 'Один/одна')
        transport_type = preferences.get('transport_type', 'Личный автомобиль')
        activity_level = preferences.get('activity_level', 'Умеренный')
        food_preference = preferences.get('food_preference', 'Кафе и рестораны')

        print(
            f"[Генератор] Доп. параметры: {traveler_type}, {transport_type}, {activity_level}, питание: {food_preference}")

        all_selected_places = []
        selected_categories = preferences.get('categories', [])

        if not selected_categories:
            selected_categories = self.db.get_all_categories()

        if 'Семья с детьми' in traveler_type:
            all_places = self.db.get_all_places()
            for place in all_places:
                place_name = place['name'].lower()
                place_desc = place.get('description', '').lower()

                if any(word in place_name or word in place_desc
                       for word in ['экстремальный', 'опасный', 'высотный', 'рафтинг',
                                    'альпинизм', 'треккинг', 'сложный']):
                    continue

                if 'семейный' in place_desc or 'детский' in place_desc:
                    if place['category'] in selected_categories:
                        all_selected_places.append(place)
                elif place['category'] in selected_categories:
                    all_selected_places.append(place)
        else:
            for category in selected_categories:
                places = self.db.get_places_by_category(category)
                all_selected_places.extend(places)

        if 'Общественный транспорт' in transport_type:
            filtered_places = []
            for place in all_selected_places:
                city = place.get('city', '')
                if 'Кызыл' in city or 'близ Кызыла' in city:
                    filtered_places.append(place)
                elif place['name'] in ['Национальный музей Республики Тыва',
                                       'Площадь Арата',
                                       'Буддийский монастырь Цеченлинг']:
                    filtered_places.append(place)
            all_selected_places = filtered_places

        if 'Спокойный' in activity_level:
            filtered_places = []
            for place in all_selected_places:
                place_name = place['name'].lower()
                if not any(word in place_name for word in ['треккинг', 'альпинизм',
                                                           'рафтинг', 'активный']):
                    filtered_places.append(place)
            all_selected_places = filtered_places
        elif 'Экстремальный' in activity_level:
            active_places = []
            for place in all_selected_places:
                place_name = place['name'].lower()
                place_desc = place.get('description', '').lower()
                if any(word in place_name or word in place_desc
                       for word in ['активный', 'экстремальный', 'треккинг',
                                    'альпинизм', 'рафтинг', 'горный']):
                    active_places.append(place)
            if active_places:
                all_selected_places = active_places

        season = preferences.get('season', 'круглый год').lower()
        if season != 'круглый год':
            filtered_places = []
            for place in all_selected_places:
                place_season = place.get('season', 'круглый год')
                if season in place_season or place_season == 'круглый год':
                    filtered_places.append(place)
            all_selected_places = filtered_places

        if 'Гастрономический тур' in food_preference:
            gastro_categories = ['гастрономия', 'этнография']
            for category in gastro_categories:
                if category not in selected_categories:
                    places = self.db.get_places_by_category(category)
                    all_selected_places.extend(places)
        elif 'Национальная кухня' in food_preference:
            for place in self.db.get_all_places():
                place_desc = place.get('description', '').lower()
                if any(word in place_desc for word in ['кухня', 'еда', 'питание',
                                                       'дегустация', 'национальный']):
                    if place not in all_selected_places:
                        all_selected_places.append(place)

        budget = preferences.get('budget', 10000)
        days = preferences.get('days', 1)

        food_cost_per_day = 0
        if 'Экономный вариант' in food_preference:
            food_cost_per_day = 500
        elif 'Кафе и рестораны' in food_preference:
            food_cost_per_day = 1000
        elif 'Гастрономический тур' in food_preference:
            food_cost_per_day = 2000
        elif 'Национальная кухня' in food_preference:
            food_cost_per_day = 1500

        total_food_cost = food_cost_per_day * days
        budget_for_places = budget - total_food_cost

        print(f"[Генератор] Бюджет: {budget} руб")
        print(f"[Генератор] На питание: {total_food_cost} руб ({food_cost_per_day}/день)")
        print(f"[Генератор] На места: {budget_for_places} руб")

        all_selected_places.sort(key=lambda x: x['cost'])

        affordable_places = []
        current_cost = 0
        max_places_per_day = 4

        if 'Спокойный' in activity_level:
            max_places_per_day = 2
        elif 'Активный' in activity_level:
            max_places_per_day = 5
        elif 'Экстремальный' in activity_level:
            max_places_per_day = 3

        max_total_places = days * max_places_per_day

        for place in all_selected_places:
            if current_cost + place['cost'] <= budget_for_places * 0.7: 
                affordable_places.append(place)
                current_cost += place['cost']
                if len(affordable_places) >= max_total_places:
                    break

        route_by_days = []
        current_day = []
        day_hours = 0
        day_places_count = 0

        for place in affordable_places:
            place_hours = place.get('time_required', 2)

            max_hours_per_day = 8
            if 'Спокойный' in activity_level:
                max_hours_per_day = 6
            elif 'Экстремальный' in activity_level:
                max_hours_per_day = 10

            if (day_hours + place_hours <= max_hours_per_day and
                    day_places_count < max_places_per_day):
                current_day.append(place)
                day_hours += place_hours
                day_places_count += 1
            else:
                if current_day:
                    route_by_days.append(current_day)
                current_day = [place]
                day_hours = place_hours
                day_places_count = 1

        if current_day:
            route_by_days.append(current_day)

        final_route = route_by_days[:days]

        print(f"[Генератор] Сгенерировано {len(final_route)} дней маршрута")
        return final_route

    def calculate_route_stats(self, route):
        total_cost = 0
        total_hours = 0
        total_places = 0
        places_by_category = {}

        for day in route:
            for place in day:
                total_cost += place['cost']
                total_hours += place.get('time_required', 2)
                total_places += 1

                category = place['category']
                places_by_category[category] = places_by_category.get(category, 0) + 1

        return {
            'total_cost': total_cost,
            'total_hours': total_hours,
            'total_places': total_places,
            'days': len(route),
            'avg_cost_per_day': total_cost / len(route) if route else 0,
            'places_by_category': places_by_category
        }

    def get_recommendations(self, route, preferences):
        recommendations = []

        traveler_type = preferences.get('traveler_type', '')
        transport_type = preferences.get('transport_type', '')
        activity_level = preferences.get('activity_level', '')
        food_preference = preferences.get('food_preference', '')
        season = preferences.get('season', '')

        if 'Семья с детьми' in traveler_type:
            recommendations.append(
                "👨‍👩‍👧‍👦 Для семьи с детьми: возьмите воду и перекусы, планируйте больше времени на отдых.")
            recommendations.append("🎒 Проверьте наличие детских комнат и игровых площадок в местах посещения.")

        if 'Пара' in traveler_type:
            recommendations.append(
                "💑 Романтическое путешествие: рассмотрите места для красивых фото и уединённого отдыха.")

        if 'Общественный транспорт' in transport_type:
            recommendations.append("🚌 При использовании общественного транспорта: уточняйте расписание заранее.")
            recommendations.append("📍 Рассматривайте маршруты в радиусе 50 км от Кызыла для удобства перемещений.")

        if 'Пешие прогулки' in transport_type:
            recommendations.append("🚶 Для пеших прогулок: выберите удобную обувь и учтите погодные условия.")

        if 'Экстремальный' in activity_level:
            recommendations.append("⚠️ Экстремальный отдых: проверьте экипировку и убедитесь в своей подготовке.")
            recommendations.append("🏔️ Учитывайте погодные условия и наличие гидов для сложных маршрутов.")

        if 'Спокойный' in activity_level:
            recommendations.append("☕ Спокойный отдых: запланируйте время для отдыха между посещениями.")

        if 'Гастрономический тур' in food_preference:
            recommendations.append("🍽️ Гастрономический тур: попробуйте национальные блюда Тывы - боорзаки, хан.")
            recommendations.append("🏪 Посетите местные рынки для покупки традиционных продуктов.")

        if 'Национальная кухня' in food_preference:
            recommendations.append("🥘 Для знакомства с национальной кухней: посетите юрточные кафе и местные столовые.")

        if 'зима' in season.lower():
            recommendations.append("❄️ Зимой: возьмите тёплую одежду, проверяйте дорожные условия.")
            recommendations.append("⛄ Зимние активности: катание на санках, лыжах, зимняя рыбалка.")
            
        elif 'лето' in season.lower():
            recommendations.append("☀️ Летом: солнцезащитный крем, головной убор и вода обязательны.")
            recommendations.append("🏊 Летние активности: купание в озёрах, пикники на природе.")

        recommendations.append("💰 Всегда имейте с собой наличные деньги - не везде есть терминалы.")
        recommendations.append("🏨 Бронируйте жильё заранее, особенно в высокий сезон (июль-август).")
        recommendations.append("📱 Сохраните офлайн-карты местности для навигации.")
        recommendations.append("🙏 Уважайте местные традиции, обычаи и священные места.")

        return recommendations[:6]

    def generate_sample_routes(self):
        samples = [
            {
                'name': 'Классическая Тыва за 3 дня',
                'preferences': {
                    'days': 3,
                    'budget': 8000,
                    'categories': ['музей', 'архитектура', 'природа'],
                    'season': 'Лето',
                    'traveler_type': 'Пара',
                    'transport_type': 'Личный автомобиль',
                    'activity_level': 'Умеренный',
                    'food_preference': 'Кафе и рестораны'
                }
            },
            {
                'name': 'Семейный уикенд на 2 дня',
                'preferences': {
                    'days': 2,
                    'budget': 5000,
                    'categories': ['природа', 'музей'],
                    'season': 'Лето',
                    'traveler_type': 'Семья с детьми',
                    'transport_type': 'Личный автомобиль',
                    'activity_level': 'Спокойный',
                    'food_preference': 'Экономный вариант'
                }
            },
            {
                'name': 'Активный тур на 4 дня',
                'preferences': {
                    'days': 4,
                    'budget': 15000,
                    'categories': ['природа', 'активный отдых'],
                    'season': 'Лето',
                    'traveler_type': 'Компания друзей',
                    'transport_type': 'Арендованный автомобиль',
                    'activity_level': 'Активный',
                    'food_preference': 'Национальная кухня'
                }
            },
            {
                'name': 'Гастрономический тур на 3 дня',
                'preferences': {
                    'days': 3,
                    'budget': 12000,
                    'categories': ['гастрономия', 'этнография'],
                    'season': 'Круглый год',
                    'traveler_type': 'Пара',
                    'transport_type': 'Личный автомобиль',
                    'activity_level': 'Умеренный',
                    'food_preference': 'Гастрономический тур'
                }
            }
        ]

        sample_results = []
        for sample in samples:
            route = self.generate_route(sample['preferences'])
            stats = self.calculate_route_stats(route)
            sample['route'] = route
            sample['stats'] = stats
            sample_results.append(sample)

        return sample_results