import sqlite3
import random
import aiohttp
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера с хранилищем состояний
API_TOKEN = 'YOUR_BOT_TOKEN'  # Замените на ваш токен от @BotFather
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # Хранилище для состояний FSM
dp = Dispatcher(storage=storage)

# Инициализация базы данных
def init_db():
    """
    Инициализация базы данных SQLite.
    Создает таблицу для хранения цитат, если она не существует,
    и добавляет начальные цитаты, если база пуста.
    """
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    
    # Создание таблицы цитат, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        author TEXT NOT NULL
    )
    ''')
    
    # Проверка, есть ли в базе начальные данные
    cursor.execute('SELECT COUNT(*) FROM quotes')
    count = cursor.fetchone()[0]
    
    # Добавление начальных цитат, если база пуста
    if count == 0:
        initial_quotes = [
            ("Жизнь — это то, что случается с нами, пока мы строим планы на будущее.", "Джон Леннон"),
            ("Мы сами должны стать теми переменами, которые хотим видеть в мире.", "Махатма Ганди"),
            ("Никогда не поздно стать тем, кем вы могли бы быть.", "Джордж Элиот"),
            ("Все, что имеет начало, имеет и конец.", "Будда"),
            ("Если ты не готов рисковать необычным, тебе придется довольствоваться обычным.", "Джим Рон")
        ]
        cursor.executemany('INSERT INTO quotes (text, author) VALUES (?, ?)', initial_quotes)
    
    conn.commit()
    conn.close()
    logging.info("База данных инициализирована")

# Инициализация базы данных при запуске
init_db()

# Определение состояний для конечного автомата (FSM)
class Form(StatesGroup):
    """
    Класс для управления состояниями бота.
    Используется для отслеживания диалога с пользователем
    (например, ожидание ввода имени автора).
    """
    waiting_for_author = State()  # Состояние ожидания ввода автора

# Обработчик команды /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение и объясняет доступные команды.
    """
    await message.answer(
        "Привет! Я бот с цитатами. Используйте следующие команды:\n"
        "/quote - получить случайную цитату\n"
        "/author - выбрать автора цитаты\n"
        "/refresh - обновить базу данных цитат из API (дополнительно)"
    )

# Обработчик команды /quote
@dp.message(Command('quote'))
async def cmd_quote(message: types.Message):
    """
    Обработчик команды /quote.
    Отправляет случайную цитату из базы данных.
    """
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    
    # Получаем случайную цитату из базы данных
    cursor.execute('SELECT text, author FROM quotes ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    
    if result:
        quote_text, quote_author = result
        await message.answer(f"«{quote_text}»\n\n— {quote_author}")
    else:
        await message.answer("К сожалению, в базе данных нет цитат. Попробуйте добавить их или обновить базу.")

# Обработчик команды /author
@dp.message(Command('author'))
async def cmd_author(message: types.Message, state: FSMContext):
    """
    Обработчик команды /author.
    Запрашивает у пользователя имя автора и переводит бота в состояние ожидания ввода.
    """
    await message.answer("Введите имя автора, чтобы получить его цитату:")
    # Устанавливаем состояние ожидания ввода имени автора
    await state.set_state(Form.waiting_for_author)

# Обработчик ввода имени автора (активируется в состоянии waiting_for_author)
@dp.message(Form.waiting_for_author)
async def process_author(message: types.Message, state: FSMContext):
    """
    Обработчик ввода имени автора.
    Активируется, когда бот находится в состоянии ожидания имени автора.
    Ищет цитаты указанного автора в базе данных и отправляет случайную цитату.
    """
    # Получаем введенное пользователем имя автора
    author_name = message.text.strip()
    
    # Сбрасываем состояние (выходим из режима ожидания ввода)
    await state.clear()
    
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    
    # Ищем автора в базе данных (используем LIKE для частичного совпадения)
    cursor.execute('SELECT COUNT(*) FROM quotes WHERE LOWER(author) LIKE LOWER(?)', (f'%{author_name}%',))
    count = cursor.fetchone()[0]
    
    if count == 0:
        await message.answer(f"Цитаты автора \"{author_name}\" не найдены в базе данных.")
        conn.close()
        return
    
    # Получаем случайную цитату указанного автора
    cursor.execute('SELECT text, author FROM quotes WHERE LOWER(author) LIKE LOWER(?) ORDER BY RANDOM() LIMIT 1', 
                  (f'%{author_name}%',))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        quote_text, quote_author = result
        await message.answer(f"«{quote_text}»\n\n— {quote_author}")
    else:
        await message.answer(f"Произошла ошибка при поиске цитат автора \"{author_name}\".")

# Функция для получения цитат из внешнего API
async def fetch_quotes_from_api():
    """
    Функция для получения цитат из внешнего API.
    Возвращает словарь с текстом цитаты и именем автора или None в случае ошибки.
    
    Примечание: API может быть недоступен или изменить формат ответа.
    В этом случае попробуйте использовать другой API для цитат.
    """
    # Пример API для получения цитат (ZenQuotes API)
    api_url = "https://zenquotes.io/api/random"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and isinstance(data, list) and len(data) > 0:
                        quote = data[0]
                        return {
                            'text': quote.get('q', '').strip(),
                            'author': quote.get('a', 'Неизвестный автор').strip()
                        }
                    else:
                        logging.error("Ошибка в формате ответа API")
                        return None
                else:
                    logging.error(f"API ответил с кодом: {response.status}")
                    return None
        except Exception as e:
            logging.error(f"Ошибка при получении цитаты из API: {e}")
            return None

# Обработчик команды /refresh для обновления базы цитат из API
@dp.message(Command('refresh'))
async def cmd_refresh(message: types.Message):
    """
    Обработчик команды /refresh.
    Получает новые цитаты из внешнего API и добавляет их в базу данных.
    """
    await message.answer("Начинаю обновление базы данных цитат...")
    
    # Получаем несколько цитат из API
    quotes_to_add = []
    success_count = 0
    
    for _ in range(5):  # Пытаемся добавить 5 новых цитат
        quote = await fetch_quotes_from_api()
        if quote and quote['text'] and quote['author']:
            quotes_to_add.append((quote['text'], quote['author']))
            success_count += 1
    
    if quotes_to_add:
        conn = sqlite3.connect('quotes.db')
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO quotes (text, author) VALUES (?, ?)', quotes_to_add)
        conn.commit()
        conn.close()
        
        await message.answer(f"База данных обновлена! Добавлено {success_count} новых цитат.")
    else:
        await message.answer("Не удалось получить новые цитаты из API. Пожалуйста, попробуйте позже или используйте другой API.")

# Обработчик для отмены текущей операции
@dp.message(Command('cancel'))
@dp.message(lambda message: message.text and message.text.lower() == 'отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Обработчик команды отмены.
    Позволяет пользователю выйти из любого состояния.
    """
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await message.answer("Операция отменена.")
    else:
        await message.answer("Нет активных операций для отмены.")

# Функция для запуска бота
async def main():
    # Запускаем бота
    logging.info("Бот запущен")
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())