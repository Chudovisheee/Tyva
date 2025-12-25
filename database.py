import sqlite3
import json
import os
from datetime import datetime


class Database:
    def __init__(self, db_name='tyva_tourism.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row  # Чтобы получать словари
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_sample_data()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                time_required INTEGER,
                cost INTEGER DEFAULT 0,
                season TEXT,
                city TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Таблица маршрутов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                places_ids TEXT,
                total_days INTEGER,
                total_cost INTEGER,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_id INTEGER,
                user_email TEXT,
                rating INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def insert_sample_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM places")
        if self.cursor.fetchone()[0] > 0:
            return

        places = [
            ('Национальный музей Республики Тыва', 'музей',
             'Крупнейший музей республики с уникальными археологическими находками, в том числе скифским золотом.',
             3, 350, 'круглый год', 'Кызыл'),

            ('Музей политических репрессий', 'музей',
             'Мемориальный комплекс, посвященный жертвам политических репрессий в Туве.',
             2, 200, 'круглый год', 'Кызыл'),

            ('Музей Н.К. Рериха', 'музей',
             'Музей, посвященный пребыванию Николая Рериха в Туве и его исследованиям.',
             2, 250, 'круглый год', 'Кызыл'),

            ('Озеро Торе-Холь', 'природа',
             'Живописное пресноводное озеро на границе с Монголией. Идеально для кемпинга, фотографирования и купания.',
             5, 0, 'лето', 'Эрзинский район'),

            ('Гора Хайыракан', 'природа',
             'Священная гора высотой 1042 м. По легендам, обладает особой энергетикой и является местом силы.',
             4, 0, 'лето, осень', 'Улуг-Хемский район'),

            ('Священная лиственница', 'природа',
             'Дерево возрастом более 1000 лет. Место паломничества и проведения обрядов.',
             1, 0, 'круглый год', 'близ Кызыла'),

            ('Скала "Спящий Лев"', 'природа',
             'Природное скальное образование, напоминающее спящего льва. Популярное место для фотосессий.',
             2, 0, 'лето, осень', 'Барун-Хемчикский район'),

            ('Река Енисей (Улуг-Хем)', 'природа',
             'Великая сибирская река. Места для рыбалки, рафтинга и пикников.',
             3, 0, 'лето', 'по всей республике'),

            ('Площадь Арата', 'архитектура',
             'Центральная площадь столицы с памятником "Центр Азии", архитектурным ансамблем и фонтанами.',
             1, 0, 'круглый год', 'Кызыл'),

            ('Буддийский храм "Цеченлинг"', 'архитектура',
             'Современный буддийский храм в тибетском стиле. Впечатляющая архитектура и умиротворенная атмосфера.',
             2, 0, 'круглый год', 'Кызыл'),

            ('Буддийский монастырь "Цеченлинг"', 'религия',
             'Действующий монастырь в центре Кызыла. Можно посетить молебен, увидеть буддийскую архитектуру.',
             2, 0, 'круглый год', 'Кызыл'),

            ('Православный храм в Кызыле', 'религия',
             'Красивый православный храм, построенный в традиционном русском стиле.',
             1, 0, 'круглый год', 'Кызыл'),
            
            ('Аржан Чойган', 'оздоровление',
             'Знаменитый минеральный источник с целебной водой. Есть купели и места для отдыха.',
             2, 600, 'круглый год', 'Тандинский район'),

            ('Горячий источник "Уш-Белдир"', 'оздоровление',
             'Термальные источники с температурой воды +52°C. Есть бассейны и гостиница.',
             4, 1200, 'круглый год', 'Кызылский район'),

            ('Спа-отель "Тайга"', 'оздоровление',
             'Комплекс для оздоровления с банями, массажем и фитотерапией.',
             3, 1500, 'круглый год', 'Кызыл'),

            ('Верблюжья ферма "Кочевник"', 'этнография',
             'Знакомство с бытом тувинских кочевников. Катание на верблюдах, дегустация национальной кухни.',
             3, 800, 'круглый год', 'Тес-Хемский район'),

            ('Этнокультурный центр "Алдын-Булак"', 'этнография',
             'Реконструкция традиционного тувинского поселения. Мастер-классы по горловому пению.',
             3, 500, 'круглый год', 'Кызыл'),

            ('Юрточный лагерь "Степной кочевник"', 'этнография',
             'Аутентичное проживание в юртах, знакомство с культурой кочевников.',
             3, 1000, 'лето', 'Тандинский район'),

            ('Турбаза "Активный отдых"', 'активный отдых',
             'Турбаза для активного отдыха: треккинг, рафтинг, конные прогулки.',
             6, 1500, 'лето, осень', 'Тоджинский район'),

            ('Горнолыжный комплекс "Снежный барс"', 'активный отдых',
             'Горнолыжный курорт с трассами разной сложности. Работает в зимний сезон.',
             5, 2000, 'зима', 'близ Кызыла'),

            ('Рафтинг по реке Малый Енисей', 'активный отдых',
             'Экстремальный сплав по горной реке с опытными инструкторами.',
             4, 2500, 'лето', 'Тоджинский район'),

            ('Ресторан "Тувинская кухня"', 'гастрономия',
             'Ресторан национальной кухни. Дегустация традиционных блюд Тывы.',
             2, 800, 'круглый год', 'Кызыл'),

            ('Кафе "Степной кочевник"', 'гастрономия',
             'Аутентичное кафе в юрте. Блюда на открытом огне, национальные напитки.',
             2, 600, 'круглый год', 'Кызыл'),

            ('Гастрономический тур "Вкусы Тывы"', 'гастрономия',
             'Экскурсия с дегустацией местных продуктов: сыры, колбасы, чаи.',
             3, 1200, 'круглый год', 'Кызыл'),

            ('Сувенирный рынок "Тува-Арт"', 'шопинг',
             'Рынок сувениров и изделий народных промыслов: камнерезное искусство, ковры, украшения.',
             2, 0, 'круглый год', 'Кызыл'),

            ('Центр народных промыслов', 'шопинг',
             'Мастерские и магазин изделий тувинских мастеров: ювелирные изделия, кожа, войлок.',
             1, 0, 'круглый год', 'Кызыл'),

            ('Галерея современного искусства', 'искусство',
             'Выставки тувинских художников и мастеров декоративно-прикладного искусства.',
             2, 200, 'круглый год', 'Кызыл'),

            ('Театр "Тувинские мелодии"', 'искусство',
             'Концерты горлового пения, национальные танцы и музыкальные представления.',
             2, 400, 'круглый год', 'Кызыл'),

            ('Долина Царей (Пий-Хем)', 'археология',
             'Комплекс древних курганов скифского времени. Археологические раскопки ведутся до сих пор.',
             3, 250, 'лето', 'Пий-Хемский район'),

            ('Камень-оберег "Чинге-Тей"', 'археология',
             'Древний камень с петроглифами. По преданиям, исполняет желания.',
             1, 0, 'круглый год', 'Тандинский район'),

            ('Национальный театр Тувы', 'культура',
             'Современные и классические постановки на тувинском и русском языках.',
             3, 300, 'круглый год', 'Кызыл'),

            ('Парк развлечений "Сказочная Тыва"', 'семейный отдых',
             'Парк с аттракционами для детей, игровыми площадками и кафе.',
             3, 500, 'лето', 'Кызыл'),

            ('Детский музей "Мир кочевников"', 'семейный отдых',
             'Интерактивный музей для детей с игровыми зонами и мастер-классами.',
             2, 300, 'круглый год', 'Кызыл'),

            ('Смотровая площадка "Любовь навеки"', 'романтические места',
             'Живописная смотровая площадка с видом на долину Енисея. Идеальное место для фото.',
             1, 0, 'круглый год', 'близ Кызыла'),

            ('Ресторан "Романтик" с видом на реку', 'романтические места',
             'Уютный ресторан с панорамным видом, идеальный для романтического ужина.',
             2, 1000, 'круглый год', 'Кызыл')
        ]

        self.cursor.executemany('''
            INSERT INTO places (name, category, description, time_required, cost, season, city)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', places)

        test_users = [
            ('test@example.com', 'Тестовый Пользователь'),
            ('family@example.com', 'Семья Ивановых'),
            ('couple@example.com', 'Петр и Мария'),
            ('friends@example.com', 'Компания друзей'),
            ('solo@example.com', 'Индивидуальный турист')
        ]

        for email, name in test_users:
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (email, name) 
                VALUES (?, ?)
            ''', (email, name))

        self.conn.commit()
        print(f"[База данных] Загружено {len(places)} туристических мест")
        print(f"[База данных] Создано {len(test_users)} тестовых пользователей")

    def get_places_by_category(self, category):
        self.cursor.execute('SELECT * FROM places WHERE category = ? ORDER BY name', (category,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_all_categories(self):
        self.cursor.execute('SELECT DISTINCT category FROM places ORDER BY category')
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_places(self):
        self.cursor.execute('SELECT * FROM places ORDER BY name')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_place_by_id(self, place_id):
        self.cursor.execute('SELECT * FROM places WHERE id = ?', (place_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def search_places(self, query, category=None):
        sql = '''
            SELECT * FROM places 
            WHERE (name LIKE ? OR description LIKE ?)
        '''
        params = [f'%{query}%', f'%{query}%']

        if category:
            sql += ' AND category = ?'
            params.append(category)

        sql += ' ORDER BY name'
        self.cursor.execute(sql, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_places_by_season(self, season):
        self.cursor.execute('''
            SELECT * FROM places 
            WHERE season LIKE ? OR season = 'круглый год'
            ORDER BY name
        ''', (f'%{season}%',))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_places_by_city(self, city):

        self.cursor.execute('SELECT * FROM places WHERE city LIKE ? ORDER BY name', (f'%{city}%',))
        return [dict(row) for row in self.cursor.fetchall()]

    def add_new_place(self, name, category, description, time_required, cost, season, city):
        self.cursor.execute('''
            INSERT INTO places (name, category, description, time_required, cost, season, city)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, description, time_required, cost, season, city))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_place(self, place_id, name=None, category=None, description=None,
                     time_required=None, cost=None, season=None, city=None):
        updates = []
        params = []

        if name:
            updates.append("name = ?")
            params.append(name)
        if category:
            updates.append("category = ?")
            params.append(category)
        if description:
            updates.append("description = ?")
            params.append(description)
        if time_required is not None:
            updates.append("time_required = ?")
            params.append(time_required)
        if cost is not None:
            updates.append("cost = ?")
            params.append(cost)
        if season:
            updates.append("season = ?")
            params.append(season)
        if city:
            updates.append("city = ?")
            params.append(city)

        if not updates:
            return False

        params.append(place_id)
        sql = f'UPDATE places SET {", ".join(updates)} WHERE id = ?'
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_place(self, place_id):
        self.cursor.execute('DELETE FROM places WHERE id = ?', (place_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def save_route(self, user_email, places_ids, total_days, total_cost, preferences):
        self.cursor.execute('''
            INSERT INTO routes (user_email, places_ids, total_days, total_cost, preferences)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_email, json.dumps(places_ids), total_days, total_cost, json.dumps(preferences)))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user_routes(self, user_email):
        self.cursor.execute('SELECT * FROM routes WHERE user_email = ? ORDER BY created_at DESC', (user_email,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_route_details(self, route_id):
        self.cursor.execute('SELECT * FROM routes WHERE id = ?', (route_id,))
        route = self.cursor.fetchone()
        if route:
            return dict(route)
        return None

    def get_popular_places(self, limit=10):
        self.cursor.execute('SELECT * FROM places ORDER BY RANDOM() LIMIT ?', (limit,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_system_stats(self):
        stats = {}

        self.cursor.execute('SELECT COUNT(*) FROM places')
        stats['total_places'] = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT COUNT(*) FROM routes')
        stats['total_routes'] = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT COUNT(*) FROM users')
        stats['total_users'] = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT SUM(total_cost) FROM routes')
        stats['total_money_calculated'] = self.cursor.fetchone()[0] or 0

        self.cursor.execute('SELECT category, COUNT(*) as count FROM places GROUP BY category ORDER BY count DESC')
        stats['places_by_category'] = {row[0]: row[1] for row in self.cursor.fetchall()}

        self.cursor.execute('SELECT AVG(cost) FROM places WHERE cost > 0')
        stats['avg_place_cost'] = int(self.cursor.fetchone()[0] or 0)

        self.cursor.execute('''
            SELECT r.id, r.user_email, r.total_days, r.total_cost, r.created_at, 
                   COUNT(*) as places_count
            FROM routes r
            LEFT JOIN users u ON r.user_email = u.email
            GROUP BY r.id
            ORDER BY r.created_at DESC
            LIMIT 5
        ''')
        stats['recent_routes'] = [dict(row) for row in self.cursor.fetchall()]

        return stats

    def get_user_by_email(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def create_user(self, email, name=None):
        try:
            self.cursor.execute('''
                INSERT INTO users (email, name) 
                VALUES (?, ?)
            ''', (email, name))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def backup_database(self, backup_path):
        import shutil
        shutil.copy2('tyva_tourism.db', backup_path)
        return os.path.exists(backup_path)

    def close(self):
        self.conn.close()


_db_instance = None


def get_db():
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance


def init_database():
    db = get_db()
    print(f"[Инициализация БД] База данных успешно инициализирована")
    print(f"[Инициализация БД] Категории: {', '.join(db.get_all_categories())}")
    return db