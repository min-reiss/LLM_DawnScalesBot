# LLM_DawnScalesBot
##LLM telegram bot [Dawn Scales]
Репозиторий содержит скрипт телеграм-бота табакси по имени **Рассвет Чешуйки** из клана Скрытая Аллея. 

## Функциональность бота
* команды: 
   - /start (выводится приветствие и список доступных команд)
   - /model (выводит название используемой LLM)
   - /clear (чистит контекст пользователя)
* запросы пользователя пересылаются LLM, запущеной на этом компьютере, и потом ответ пересылаются пользователю

## Особенности бота
Контекст переписки сохраняется, LLM отвечает на текущий запрос с учетом контекста.

![Скриншот с LM Studio](https://github.com/min-reiss/LLM_DawnScalesBot/blob/main/pictures/DawnScales_serv.jpg)
