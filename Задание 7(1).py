# Этот код получает 5 постов с сайта JSONPlaceholder

import requests  # Библиотека для запросов

def get_posts(): # Эта функция получает посты с сайта
    
    print("Начинаем работу...")
    print("=" * 50)
    
    try:
        # 1. Отправляем запрос на сайт
        print("Пытаемся подключиться к сайту...")
        url = "https://jsonplaceholder.typicode.com/posts"  # Адрес сайта
        response = requests.get(url)  # Отправляем запрос
        
        # Проверяем, что все ок
        if response.status_code == 200:
            print("Ура! Сайт ответил успешно")
        else:
            print(f"Ой, проблема: код ошибки {response.status_code}")
            return False
        
        # 2. Получаем данные
        print("Получаем данные...")
        all_posts = response.json()  # Преобразуем ответ
        
        # 3. Смотрим сколько всего постов
        total = len(all_posts)
        print(f"Нашли {total} постов!")
        print()
        
        # 4. Показываем первые 5 постов
        print("Вот первые 5 постов:")
        print("-" * 40)
        
        # Счетчик для нумерации
        count = 1
        
        # Проходим по первым 5 постам
        for post in all_posts[:5]:
            print(f"Пост №{count}:")
            print(f"ID поста: {post['id']}")
            print(f"Автор: пользователь №{post['userId']}")
            print(f"Заголовок: {post['title']}")
            
            # Берем только начало текста 
            text = post['body']
            if len(text) > 80:
                short_text = text[:80] + "..."
            else:
                short_text = text
            print(f"Текст: {short_text}")
            
            print("-" * 40)
            count += 1  # Увеличиваем счетчик
        
        print("Программа завершила работу успешно!")
        return True
        
    except Exception as e:  # Если что-то пошло не так
        print("Ой, произошла ошибка!")
        print(f"Подробности: {e}")
        print("Проверь подключение к интернету")
        return False

# Запускаем программу
if __name__ == "__main__":
    print("Привет! Эта программа получает посты из интернета")
    print()
    
    # Запускаем нашу функцию
    result = get_posts()
    
    print()
    if result:
        print("Все прошло хорошо!")
    else:
        print("Что-то пошло не так :(")
    
    # Чтобы окно не закрылось сразу
    input("Нажми Enter чтобы выйти...")