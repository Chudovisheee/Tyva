import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import datetime


class TyvaTravelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tyva Travel Planner PRO")
        self.root.geometry("1100x650")

        self.setup_colors()
        self.setup_styles()

        self.create_widgets()

    def setup_colors(self):
        self.bg_color = "#FFFFFF"
        self.yellow_color = "#FFD700"
        self.blue_color = "#2196F3"
        self.dark_blue = "#1976D2"
        self.light_blue = "#E3F2FD"
        self.text_color = "#333333"
        self.btn_bg = "#2196F3"
        self.btn_fg = "#FFFFFF"

        self.root.configure(bg=self.bg_color)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Vertical.TScrollbar",
                        background=self.light_blue,
                        bordercolor=self.blue_color,
                        arrowcolor=self.dark_blue,
                        troughcolor="#F0F0F0")

        style.configure('Blue.TButton',
                        background=self.blue_color,
                        foreground=self.btn_fg,
                        font=('Arial', 8, 'bold'),
                        padding=5,
                        borderwidth=0)

        style.configure('Yellow.TButton',
                        background=self.yellow_color,
                        foreground='#333333',
                        font=('Arial', 8, 'bold'),
                        padding=5,
                        borderwidth=0)

    def create_widgets(self):
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # ============ ЛЕВАЯ КОЛОНКА - ПАРАМЕТРЫ ============
        left_panel = tk.Frame(main_container, bg=self.light_blue, width=500)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8))
        left_panel.pack_propagate(False)

        left_header = tk.Label(left_panel,
                               text="⚙️ ПАРАМЕТРЫ ПУТЕШЕСТВИЯ",
                               font=("Arial", 11, "bold"),
                               bg=self.blue_color,
                               fg="white",
                               pady=7)
        left_header.pack(fill=tk.X)

        left_container = tk.Frame(left_panel, bg=self.light_blue)
        left_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        left_canvas = tk.Canvas(left_container, bg=self.light_blue, highlightthickness=0)

        self.left_frame = tk.Frame(left_canvas, bg=self.light_blue)

        self.left_frame.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )

        left_canvas.create_window((0, 0), window=self.left_frame, anchor="nw")
        left_canvas.pack(side="left", fill="both", expand=True)

        def on_mouse_wheel(event):
            left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        left_canvas.bind("<MouseWheel>", on_mouse_wheel)
        self.left_frame.bind("<MouseWheel>", on_mouse_wheel)

        params_frame = tk.Frame(self.left_frame, bg=self.light_blue, padx=12, pady=10)
        params_frame.pack(fill=tk.BOTH, expand=True)

        # --- ОСНОВНЫЕ ПАРАМЕТРЫ ---
        basic_frame = tk.LabelFrame(params_frame, text=" Основные параметры ",
                                    font=("Arial", 9, "bold"),
                                    bg=self.light_blue,
                                    fg=self.dark_blue,
                                    relief=tk.GROOVE,
                                    borderwidth=1,
                                    padx=8,
                                    pady=8)
        basic_frame.pack(fill=tk.X, pady=(0, 10))

        basic_frame.grid_columnconfigure(0, weight=1, minsize=100)
        basic_frame.grid_columnconfigure(1, weight=2, minsize=180)

        row = 0

        tk.Label(basic_frame, text="Дней:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.days_var = tk.StringVar(value="3")
        days_combo = ttk.Combobox(basic_frame, textvariable=self.days_var,
                                  values=[str(i) for i in range(1, 15)],
                                  width=18, state="readonly", font=("Arial", 8))
        days_combo.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)
        row += 1

        tk.Label(basic_frame, text="Бюджет:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.budget_var = tk.StringVar(value="10000")
        budget_entry = ttk.Entry(basic_frame, textvariable=self.budget_var, width=21,
                                 font=("Arial", 8))
        budget_entry.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)
        row += 1

        tk.Label(basic_frame, text="Сезон:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.season_var = tk.StringVar(value="Лето")
        season_combo = ttk.Combobox(basic_frame, textvariable=self.season_var,
                                    values=["Лето", "Осень", "Зима", "Весна", "Круглый год"],
                                    width=18, state="readonly", font=("Arial", 8))
        season_combo.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)
        row += 1

        tk.Label(basic_frame, text="Комфорт:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.comfort_var = tk.StringVar(value="средний")
        comfort_combo = ttk.Combobox(basic_frame, textvariable=self.comfort_var,
                                     values=["эконом", "средний", "комфорт"],
                                     width=18, state="readonly", font=("Arial", 8))
        comfort_combo.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)
        row += 1

        tk.Label(basic_frame, text="Тип:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.traveler_var = tk.StringVar(value="Пара")
        traveler_combo = ttk.Combobox(basic_frame, textvariable=self.traveler_var,
                                      values=["Один/одна", "Пара", "Семья с детьми",
                                              "Компания друзей", "Групповой тур"],
                                      width=18, state="readonly", font=("Arial", 8))
        traveler_combo.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)
        row += 1

        tk.Label(basic_frame, text="Транспорт:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.transport_var = tk.StringVar(value="Личный автомобиль")
        transport_combo = ttk.Combobox(basic_frame, textvariable=self.transport_var,
                                       values=["Личный автомобиль", "Общественный транспорт",
                                               "Арендованный автомобиль", "Такси/трансферы",
                                               "Пешие прогулки"],
                                       width=18, state="readonly", font=("Arial", 8))
        transport_combo.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)
        row += 1

        tk.Label(basic_frame, text="Активность:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.activity_var = tk.StringVar(value="Умеренный")
        activity_combo = ttk.Combobox(basic_frame, textvariable=self.activity_var,
                                      values=["Спокойный", "Умеренный", "Активный", "Экстремальный"],
                                      width=18, state="readonly", font=("Arial", 8))
        activity_combo.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)
        row += 1

        tk.Label(basic_frame, text="Питание:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.food_var = tk.StringVar(value="Кафе и рестораны")
        food_combo = ttk.Combobox(basic_frame, textvariable=self.food_var,
                                  values=["Экономный вариант", "Кафе и рестораны",
                                          "Гастрономический тур", "Национальная кухня",
                                          "Без предпочтений"],
                                  width=18, state="readonly", font=("Arial", 8))
        food_combo.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)
        row += 1

        tk.Label(basic_frame, text="Email:",
                 bg=self.light_blue, font=("Arial", 8), fg=self.text_color).grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=3)
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(basic_frame, textvariable=self.email_var, width=21,
                                font=("Arial", 8))
        email_entry.grid(row=row, column=1, sticky=tk.W + tk.E, padx=4, pady=3)

        separator_frame = tk.Frame(params_frame, bg=self.blue_color, height=1)
        separator_frame.pack(fill=tk.X, pady=6)

        # --- КАТЕГОРИИ ИНТЕРЕСОВ ---
        categories_frame = tk.LabelFrame(params_frame, text=" Категории интересов ",
                                         font=("Arial", 9, "bold"),
                                         bg=self.light_blue,
                                         fg="#333333",
                                         relief=tk.GROOVE,
                                         borderwidth=1,
                                         padx=8,
                                         pady=8)
        categories_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        categories_label = tk.Label(categories_frame,
                                    text="Выберите категории:",
                                    font=("Arial", 8, "bold"),
                                    bg=self.light_blue,
                                    fg=self.text_color)
        categories_label.pack(anchor=tk.W, padx=4, pady=(0, 6))

        cat_container = tk.Frame(categories_frame, bg=self.light_blue)
        cat_container.pack(fill=tk.BOTH, expand=True)

        cat_canvas = tk.Canvas(cat_container, bg=self.light_blue, highlightthickness=0, height=150)
        cat_scrollbar = ttk.Scrollbar(cat_container, orient="vertical", command=cat_canvas.yview)
        cat_scrollable_frame = tk.Frame(cat_canvas, bg=self.light_blue)

        cat_scrollable_frame.bind(
            "<Configure>",
            lambda e: cat_canvas.configure(scrollregion=cat_canvas.bbox("all"))
        )

        cat_canvas.create_window((0, 0), window=cat_scrollable_frame, anchor="nw")
        cat_canvas.configure(yscrollcommand=cat_scrollbar.set)

        cat_canvas.pack(side="left", fill="both", expand=True)
        cat_scrollbar.pack(side="right", fill="y")

        cat_canvas.bind("<MouseWheel>", on_mouse_wheel)
        cat_scrollable_frame.bind("<MouseWheel>", on_mouse_wheel)

        self.categories_vars = {}
        categories_list = [
            "музей", "природа", "архитектура", "религия",
            "оздоровление", "этнография", "активный отдых", "гастрономия",
            "шопинг", "искусство", "археология", "культура",
            "семейный отдых", "романтические места"
        ]

        display_names = {
            "музей": "Музеи и история",
            "природа": "Природа и парки",
            "архитектура": "Архитектура",
            "религия": "Религиозные места",
            "оздоровление": "Оздоровление",
            "этнография": "Этнография",
            "активный отдых": "Активный отдых",
            "гастрономия": "Гастрономия",
            "шопинг": "Шопинг",
            "искусство": "Искусство",
            "археология": "Археология",
            "культура": "Культура",
            "семейный отдых": "Семейный отдых",
            "романтические места": "Романтические места"
        }

        for i, category in enumerate(categories_list):
            var = tk.BooleanVar(value=True if i < 2 else False)
            self.categories_vars[category] = var

            display_name = display_names.get(category, category)
            short_display = display_name[:20] + "..." if len(display_name) > 20 else display_name

            cb = tk.Checkbutton(cat_scrollable_frame,
                                text=f"  {short_display}",
                                variable=var,
                                bg=self.light_blue,
                                fg=self.text_color,
                                font=("Arial", 8),
                                anchor=tk.W,
                                width=22,
                                activebackground=self.light_blue,
                                activeforeground=self.text_color,
                                selectcolor=self.yellow_color)
            cb.pack(anchor=tk.W, padx=4, pady=1)

        generate_frame = tk.Frame(params_frame, bg=self.light_blue)
        generate_frame.pack(fill=tk.X, pady=(8, 0))

        generate_btn = tk.Button(generate_frame,
                                 text="🚀 СГЕНЕРИРОВАТЬ",
                                 command=self.generate_route,
                                 bg=self.yellow_color,
                                 fg="#333333",
                                 font=("Arial", 9, "bold"),
                                 padx=15,
                                 pady=6,
                                 borderwidth=0,
                                 cursor="hand2",
                                 activebackground="#FFC107",
                                 activeforeground="#333333")
        generate_btn.pack()

        # ============ ПРАВАЯ КОЛОНКА - МАРШРУТ ============
        right_panel = tk.Frame(main_container, bg="white", bd=1, relief=tk.RAISED, width=450)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_panel.pack_propagate(False)       

        right_header = tk.Label(right_panel,
                                text="📋 МАРШРУТ",
                                font=("Arial", 11, "bold"),
                                bg=self.blue_color,
                                fg="white",
                                pady=7)
        right_header.pack(fill=tk.X)

        text_container = tk.Frame(right_panel, bg="white")
        text_container.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.result_text = tk.Text(text_container,
                                   wrap=tk.WORD,
                                   font=("Consolas", 8),
                                   bg="white",
                                   fg=self.text_color,
                                   relief=tk.SUNKEN,
                                   borderwidth=1,
                                   padx=10,
                                   pady=10)

        text_scrollbar = ttk.Scrollbar(text_container, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=text_scrollbar.set)

        self.result_text.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")

        result_buttons_frame = tk.Frame(right_panel, bg="white")
        result_buttons_frame.pack(fill=tk.X, padx=6, pady=(0, 6))

        tk.Button(result_buttons_frame,
                  text="📄 Экспорт TXT",
                  command=self.export_txt,
                  bg=self.blue_color,
                  fg='white',
                  font=('Arial', 8, 'bold'),
                  padx=10,
                  pady=4,
                  borderwidth=0,
                  cursor='hand2',
                  activebackground=self.dark_blue,
                  activeforeground='white').pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Button(result_buttons_frame,
                  text="📄 Экспорт html",
                  command=self.export_html,
                  bg=self.blue_color,
                  fg='white',
                  font=('Arial', 8, 'bold'),
                  padx=10,
                  pady=4,
                  borderwidth=0,
                  cursor='hand2',
                  activebackground=self.dark_blue,
                  activeforeground='white').pack(side=tk.LEFT, padx=(0, 8))        

        tk.Button(result_buttons_frame,
                  text="🔄 Очистить",
                  command=self.clear_results,
                  bg=self.yellow_color,
                  fg="#333333",
                  font=('Arial', 8, 'bold'),
                  padx=10,
                  pady=4,
                  borderwidth=0,
                  cursor='hand2',
                  activebackground="#FFC107",
                  activeforeground='#333333').pack(side=tk.LEFT)

        status_bar = tk.Frame(self.root, bg=self.blue_color, height=25)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)

        left_status = tk.Frame(status_bar, bg=self.blue_color)
        left_status.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.status_var = tk.StringVar(value="✅ Готов к работе")
        status_label = tk.Label(left_status,
                                textvariable=self.status_var,
                                bg=self.blue_color,
                                fg="white",
                                font=("Arial", 8))
        status_label.pack(side=tk.LEFT, padx=10)

        right_status = tk.Frame(status_bar, bg=self.yellow_color, width=200)
        right_status.pack(side=tk.RIGHT, fill=tk.Y)
        right_status.pack_propagate(False)

        version_label = tk.Label(right_status,
                                 text="TyvaTravelPlanner PRO",
                                 bg=self.yellow_color,
                                 fg="#333333",
                                 font=("Arial", 7, "bold"))
        version_label.pack(padx=10, pady=4)

    def generate_route(self):
        try:
            self.status_var.set("⏳ Генерация...")
            self.root.update()
            
            days = int(self.days_var.get())
            budget = int(self.budget_var.get())

            season_map = {"Лето": "лето", "Осень": "осень", "Зима": "зима",
                          "Весна": "весна", "Круглый год": "круглый год"}
            season = season_map.get(self.season_var.get(), "лето")

            comfort_map = {"эконом": "эконом", "средний": "средний", "комфорт": "комфорт"}
            comfort_level = comfort_map.get(self.comfort_var.get(), "средний")

            traveler_type = self.traveler_var.get()
            transport_type = self.transport_var.get()
            activity_level = self.activity_var.get()
            food_preference = self.food_var.get()
            user_email = self.email_var.get() if self.email_var.get().strip() else None

            selected_categories = []
            for category, var in self.categories_vars.items():
                if var.get():
                    selected_categories.append(category)

            try:
                from route_generator import RouteGenerator

                generator = RouteGenerator()
                preferences = {
                    'days': days,
                    'budget': budget,
                    'categories': selected_categories,
                    'season': season,
                    'comfort_level': comfort_level,
                    'traveler_type': traveler_type,
                    'transport_type': transport_type,
                    'activity_level': activity_level,
                    'food_preference': food_preference
                }

                if user_email:
                    preferences['user_email'] = user_email

                print(f"[DEBUG] Отправляем предпочтения в бэкенд:")
                print(f"[DEBUG] categories: {selected_categories}")
                print(f"[DEBUG] Все preferences: {preferences}")

                route = generator.generate_route(preferences)

                if not route:
                    messagebox.showwarning("Внимание", "Не удалось сгенерировать маршрут с указанными параметрами.")
                    self.status_var.set("❌ Нет маршрута")
                    return

                print(f"[DEBUG] Маршрут сгенерирован: {len(route)} дней")

                stats = generator.calculate_route_stats(route)
                print(f"[DEBUG] Статистика рассчитана: {stats}")

                recommendations = generator.get_recommendations(route, preferences)
                print(f"[DEBUG] Рекомендации получены: {len(recommendations)}")

                result = "🎯 ПЕРСОНАЛИЗИРОВАННЫЙ МАРШРУТ ПО РЕСПУБЛИКЕ ТЫВА\n"
                result += "=" * 60 + "\n\n"

                result += "📋 ВАШИ ПАРАМЕТРЫ:\n"
                result += "-" * 40 + "\n"
                result += f"• Дней: {days}\n"
                result += f"• Бюджет: {budget:,} руб\n"
                result += f"• Сезон: {self.season_var.get()}\n"
                result += f"• Комфорт: {comfort_level}\n"
                result += f"• Тип путешественника: {traveler_type}\n"
                result += f"• Транспорт: {transport_type}\n"
                result += f"• Активность: {activity_level}\n"
                result += f"• Питание: {food_preference}\n"
                if user_email:
                    result += f"• Email: {user_email}\n"

                result += f"\n📊 СТАТИСТИКА МАРШРУТА:\n"
                result += "-" * 40 + "\n"
                result += f"• Дней запланировано: {stats['days']}\n"
                result += f"• Стоимость посещений: {stats['total_cost']:,} руб\n"
                result += f"• Общее время: {stats['total_hours']} часов\n"
                result += f"• Количество мест: {stats['total_places']}\n"

                if stats.get('places_by_category'):
                    result += f"\n🏷️ РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ:\n"
                    for category, count in stats['places_by_category'].items():
                        result += f"  • {category}: {count} мест(а)\n"

                result += f"\n📅 ПЛАН ПО ДНЯМ:\n"
                result += "=" * 60 + "\n"

                for day_num, day_places in enumerate(route, 1):
                    if not day_places:
                        continue

                    day_cost = sum(place['cost'] for place in day_places)
                    day_hours = sum(place.get('time_required', 2) for place in day_places)

                    result += f"\nДЕНЬ {day_num}:\n"
                    result += f"  💰 Стоимость: {day_cost:,} руб\n"
                    result += f"  ⏱️  Время: {day_hours} часов\n"
                    result += f"  📍 Мест: {len(day_places)}\n"
                    result += "-" * 40 + "\n"

                    for place in day_places:
                        result += f"  • {place['name']}\n"
                        result += f"    🏷️  {place['category']} | 📍 {place['city']}\n"
                        result += f"    💰 {place['cost']} руб | ⏱️  {place.get('time_required', 2)} ч\n"
                        if place.get('description'):
                            result += f"    📝 {place['description']}\n"
                        result += f"{place['link']}\n"
                        result += "\n"

                if recommendations:
                    result += f"\n💡 РЕКОМЕНДАЦИИ:\n"
                    result += "-" * 40 + "\n"
                    for rec in recommendations:
                        result += f"• {rec}\n"

                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(1.0, result)
                self.status_var.set(f"✅ Маршрут сгенерирован! Стоимость: {stats['total_cost']:,} руб")

                self.last_route = route
                self.last_stats = stats
                self.last_preferences = preferences

            except ImportError as e:
                print(f"[DEBUG] Ошибка импорта: {e}")
                
            except Exception as e:
                print(f"[DEBUG] Ошибка в generate_route: {e}")
                raise

        except Exception as e:
            print(f"[DEBUG] Общая ошибка: {e}")
            messagebox.showerror("Ошибка", f"Ошибка генерации: {str(e)}")
            self.status_var.set("❌ Ошибка генерации")

    def export_txt(self):
        if not hasattr(self, 'last_route'):
            messagebox.showwarning("Внимание", "Сначала сгенерируйте маршрут")
            return

        try:
            from export import export_route

            user_email = self.email_var.get().strip() if self.email_var.get() else None

            filepath = export_route(self.last_route, self.last_stats,
                                    self.last_preferences, format='txt',
                                    user_email=user_email)

            messagebox.showinfo("Успех", f"Текстовый файл сохранен:\n{filepath}")
            self.status_var.set(f"📄 Экспортировано в TXT")

        except ImportError:
            print(f"[DEBUG] Ошибка импорта: {e}")
            
    def export_html(self):
        if not hasattr(self, 'last_route'):
            messagebox.showwarning("Внимание", "Сначала сгенерируйте маршрут")
            return

        try:
            from export import export_route

            user_email = self.email_var.get().strip() if self.email_var.get() else None

            filepath = export_route(self.last_route, self.last_stats,
                                    self.last_preferences, format='html',
                                    user_email=user_email)
            messagebox.showinfo("Успех", f"html сохранен:\n{filepath}")
            self.status_var.set(f"📄 Экспортировано в html")
            
            import webbrowser
            webbrowser.open(f'file://{os.path.abspath(filepath)}')            


        except ImportError:
            print(f"[DEBUG] Ошибка импорта: {e}")    
            
            
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("✅ Готов к работе")
        if hasattr(self, 'last_route'):
            del self.last_route
        if hasattr(self, 'last_stats'):
            del self.last_stats
        if hasattr(self, 'last_preferences'):
            del self.last_preferences


def main():
    root = tk.Tk()
    app = TyvaTravelGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()