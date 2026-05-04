import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Загрузка данных
        self.quotes_file = "quotes.json"
        self.history_file = "history.json"
        self.quotes = self.load_quotes()
        self.history = self.load_history()
        
        # Создание GUI
        self.create_widgets()
        self.refresh_author_filter()
        self.refresh_topic_filter()
        self.refresh_history_list()
        
    def load_quotes(self):
        """Загрузка цитат из JSON или создание стандартных"""
        default_quotes = [
            {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
            {"text": "Жизнь - это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Философия"},
            {"text": "Единственный способ делать великую работу - любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Карьера"},
            {"text": "Не суди по ошибкам других, если и сам не безгрешен.", "author": "Конфуций", "topic": "Мудрость"},
            {"text": "В двух словах: бери и делай!", "author": "Ричард Брэнсон", "topic": "Мотивация"},
            {"text": "Знание - сила.", "author": "Фрэнсис Бэкон", "topic": "Образование"},
            {"text": "Красота спасёт мир.", "author": "Фёдор Достоевский", "topic": "Искусство"},
            {"text": "Всё, что нас не убивает, делает нас сильнее.", "author": "Фридрих Ницше", "topic": "Философия"},
        ]
        
        if os.path.exists(self.quotes_file):
            with open(self.quotes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            with open(self.quotes_file, 'w', encoding='utf-8') as f:
                json.dump(default_quotes, f, ensure_ascii=False, indent=2)
            return default_quotes
    
    def save_quotes(self):
        """Сохранение цитат в JSON"""
        with open(self.quotes_file, 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=2)
    
    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        """Сохранение истории в JSON"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        # Основной фрейм для цитаты
        self.quote_frame = tk.LabelFrame(self.root, text="Случайная цитата", padx=10, pady=10)
        self.quote_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.quote_label = tk.Label(self.quote_frame, text="Нажмите кнопку для генерации цитаты", 
                                     wraplength=750, font=("Arial", 12), justify="center")
        self.quote_label.pack(pady=20)
        
        self.author_label = tk.Label(self.quote_frame, text="", font=("Arial", 10, "italic"))
        self.author_label.pack()
        
        # Кнопки управления
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)
        
        self.generate_btn = tk.Button(self.button_frame, text="Сгенерировать цитату", 
                                      command=self.generate_quote, bg="#4CAF50", fg="white",
                                      font=("Arial", 10, "bold"), padx=10, pady=5)
        self.generate_btn.pack(side="left", padx=5)
        
        self.add_quote_btn = tk.Button(self.button_frame, text="Добавить цитату", 
                                       command=self.add_quote_dialog, bg="#2196F3", fg="white",
                                       font=("Arial", 10), padx=10, pady=5)
        self.add_quote_btn.pack(side="left", padx=5)
        
        # Фрейм фильтров
        self.filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        self.filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по автору
        tk.Label(self.filter_frame, text="Автор:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.author_filter_var = tk.StringVar(value="Все")
        self.author_filter_combo = ttk.Combobox(self.filter_frame, textvariable=self.author_filter_var, 
                                                state="readonly", width=30)
        self.author_filter_combo.grid(row=0, column=1, padx=5, pady=5)
        self.author_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history())
        
        # Фильтр по теме
        tk.Label(self.filter_frame, text="Тема:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.topic_filter_var = tk.StringVar(value="Все")
        self.topic_filter_combo = ttk.Combobox(self.filter_frame, textvariable=self.topic_filter_var,
                                               state="readonly", width=30)
        self.topic_filter_combo.grid(row=0, column=3, padx=5, pady=5)
        self.topic_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history())
        
        # Кнопка сброса фильтров
        self.reset_btn = tk.Button(self.filter_frame, text="Сбросить фильтры", 
                                   command=self.reset_filters, bg="#FF9800")
        self.reset_btn.grid(row=0, column=4, padx=10, pady=5)
        
        # Фрейм истории
        self.history_frame = tk.LabelFrame(self.root, text="История цитат", padx=10, pady=5)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Список истории с прокруткой
        self.history_listbox = tk.Listbox(self.history_frame, height=10, font=("Arial", 9))
        self.history_scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", 
                                               command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=self.history_scrollbar.set)
        
        self.history_listbox.pack(side="left", fill="both", expand=True)
        self.history_scrollbar.pack(side="right", fill="y")
        
        # Информационная метка
        self.info_label = tk.Label(self.root, text=f"Всего цитат: {len(self.quotes)} | История: {len(self.history)}",
                                   font=("Arial", 8), fg="gray")
        self.info_label.pack(side="bottom", pady=2)
    
    def generate_quote(self):
        """Генерация случайной цитаты"""
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Сначала добавьте цитаты!")
            return
        
        quote = random.choice(self.quotes)
        self.quote_label.config(text=f"\"{quote['text']}\"")
        self.author_label.config(text=f"— {quote['author']} (Тема: {quote['topic']})")
        
        # Сохранение в историю
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": quote['text'],
            "author": quote['author'],
            "topic": quote['topic']
        }
        self.history.append(history_entry)
        self.save_history()
        self.filter_history()
        self.update_info()
    
    def add_quote_dialog(self):
        """Диалог добавления новой цитаты"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить цитату")
        dialog.geometry("500x300")
        dialog.grab_set()
        
        tk.Label(dialog, text="Текст цитаты:", font=("Arial", 10, "bold")).pack(pady=(10,0))
        text_entry = tk.Text(dialog, height=5, width=60)
        text_entry.pack(pady=5)
        
        tk.Label(dialog, text="Автор:", font=("Arial", 10, "bold")).pack(pady=(10,0))
        author_entry = tk.Entry(dialog, width=50)
        author_entry.pack(pady=5)
        
        tk.Label(dialog, text="Тема:", font=("Arial", 10, "bold")).pack(pady=(10,0))
        topic_entry = tk.Entry(dialog, width=50)
        topic_entry.pack(pady=5)
        
        def save_quote():
            text = text_entry.get("1.0", tk.END).strip()
            author = author_entry.get().strip()
            topic = topic_entry.get().strip()
            
            # Проверка на пустые строки
            if not text:
                messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
                return
            if not author:
                messagebox.showerror("Ошибка", "Автор не может быть пустым!")
                return
            if not topic:
                messagebox.showerror("Ошибка", "Тема не может быть пустой!")
                return
            
            # Добавление цитаты
            self.quotes.append({"text": text, "author": author, "topic": topic})
            self.save_quotes()
            self.update_info()
            self.refresh_author_filter()
            self.refresh_topic_filter()
            
            messagebox.showinfo("Успех", "Цитата успешно добавлена!")
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save_quote, bg="#4CAF50", fg="white",
                 padx=20, pady=5).pack(pady=20)
    
    def refresh_author_filter(self):
        """Обновление списка авторов в фильтре"""
        authors = sorted(set(quote['author'] for quote in self.quotes))
        self.author_filter_combo['values'] = ["Все"] + authors
        self.author_filter_var.set("Все")
    
    def refresh_topic_filter(self):
        """Обновление списка тем в фильтре"""
        topics = sorted(set(quote['topic'] for quote in self.quotes))
        self.topic_filter_combo['values'] = ["Все"] + topics
        self.topic_filter_var.set("Все")
    
    def filter_history(self):
        """Фильтрация истории по автору и теме"""
        self.history_listbox.delete(0, tk.END)
        
        selected_author = self.author_filter_var.get()
        selected_topic = self.topic_filter_var.get()
        
        filtered = self.history
        if selected_author != "Все":
            filtered = [h for h in filtered if h['author'] == selected_author]
        if selected_topic != "Все":
            filtered = [h for h in filtered if h['topic'] == selected_topic]
        
        if not filtered:
            self.history_listbox.insert(tk.END, "Нет цитат, соответствующих фильтрам")
        else:
            for item in filtered:
                display_text = f"[{item['timestamp']}] {item['author']}: {item['text'][:80]}..."
                self.history_listbox.insert(tk.END, display_text)
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.author_filter_var.set("Все")
        self.topic_filter_var.set("Все")
        self.filter_history()
    
    def refresh_history_list(self):
        """Обновление списка истории (без фильтрации)"""
        self.filter_history()
    
    def update_info(self):
        """Обновление информационной панели"""
        self.info_label.config(text=f"Всего цитат: {len(self.quotes)} | История: {len(self.history)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()