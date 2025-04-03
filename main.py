import telebot
from telebot.types import Message
import requests
import jsons
import datetime
import random
from Class_ModelResponse import ModelResponse


API_TOKEN = 'YOUR_TG_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)


def cat_speech(text):
    
    # Список кошачьих звуков и окончаний
    cat_noises = ['мяу', 'мурр', 'мя', 'мрр', 'мур-мяу', 'мррр']
    endings = ['!', '', '~']
    
    # Разбиваем текст на предложения
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    result = []
    result.append("Мрр")
    for sentence in sentences:
        # Добавляем случайное мяуканье в начало с вероятностью 70%
        if random.random() < 0.7:
            noise = random.choice(cat_noises)
            ending = random.choice(endings)
            result.append(f"{noise.capitalize()}{ending}")
        
        # Добавляем само предложение
        result.append(sentence.lower())
        
        # Добавляем кошачий звук в конец с вероятностью 50%
        if random.random() < 0.5:
            noise = random.choice(cat_noises)
            ending = random.choice(endings[:3])  # Без вопросительных знаков в конце
            result.append(f" {noise}{ending}")
    
    # Собираем результат и добавляем финальное мяуканье с вероятностью 30%
    final_text = ' '.join(result)
    if random.random() < 0.3:
        final_text += f" {random.choice(cat_noises)}..."
    
    return final_text.capitalize()
    


BOT_LOR = """ Ты - кот-табакси по имени Рассвет Чешуйки из клана Скрытая Аллея. 
         Родившись в воровском квартале Скрытой Аллеи, Рассвет с детства усвоил: мир делится на тех, кто обманывает, и тех, кого обманывают. Его «волшебные» безделушки — амулеты из позолоченной жести, «эликсиры молодости» (разбавленное вино с мятой) и «предсказания судьбы» (подстроенные под клиента) — пользовались бешеным успехом у богатых простаков.
         Но в отличие от других мошенников, он никогда не трогал бедняков. 
         Ты очень общительный и всегда готов помочь людям своими знаниями.
         Ты умный, но иногда ленивый. 
         Отвечай с кошачьими манерностями, иногда вставляй "мяу", "мурр" и другие звуки. 
        """
# Команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я ваш Рассвет Чешуйки.\n"
        "Доступные команды:\n"
        "/start - вывод всех доступных команд\n"
        "/model - выводит название используемой языковой модели\n"
        "/clear - отчищает контекст пользователя\n"
        "Отправьте любое сообщение, и я отвечу с помощью LLM модели."
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['model'])
def send_model_name(message):
    # Отправляем запрос к LM Studio для получения информации о модели
    response = requests.get('http://localhost:1234/v1/models')

    if response.status_code == 200:
        model_info = response.json()
        model_name = model_info['data'][0]['id']
        bot.reply_to(message, f"Используемая модель: {model_name}")
    else:
        bot.reply_to(message, 'Не удалось получить информацию о модели.')

@bot.message_handler(commands=['clear'])
def send_model_name(message):
    user_id = message.from_user.id
    if user_id in user_message_history:
        del user_message_history[user_id]
        bot.reply_to(message, cat_speech('Прощай, я сотру тебя из памяти'))
    else:
        bot.reply_to(message, cat_speech('Упси-дупси'))



user_message_history = {}
@bot.message_handler(func=lambda message: True)
def handle_message(message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id not in user_message_history:
        user_message_history[user_id] = [
            {"role": "assistant", "content": BOT_LOR},  # Лор бота
            {"role": "system", "content": "Ты всегда отвечаешь как кот-табакси Шашлык"}
        ]

    # Получаем историю сообщений текущего пользователя
    user_history = user_message_history.get(user_id, [])

    user_history.append({"role": "user", "content": message.text})

    #  Добавим в контест текущую дату и время
    current_date_time = datetime.datetime.now().strftime("%d %B %Y, %H:%M MSK")
    messages = [ 
                { 
                    "role": "system", 
                    "content": f"Текущая дата: {current_date_time}"
                } ]
    
    for msg in user_history:
        messages.append(msg)

    bot.send_chat_action(chat_id, "typing")     # Симулируем что бот печатает ответ

    #user_query = message.text
    request = {
        "messages": messages
    }
    response = requests.post(
        'http://localhost:1234/v1/chat/completions',
        json=request
    )

    if response.status_code == 200:
        model_response :ModelResponse = jsons.loads(response.text, ModelResponse)
        reply = model_response.choices[0].message.content
        # Добавляем ответ бота в историю пользователя
        user_history.append({"role": "assistant", "content": reply})
        # Сохраняем усеченную историю
        user_message_history[user_id] = user_history[-30:]
        bot.reply_to(message, reply)
    else:
        txt = cat_speech('Произошла ошибка при обращении к модели.')
        bot.reply_to(message, txt)
    
    print('do')



# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)