import telebot, wikipedia, re, random
# Создаем экземпляр бота
bot = telebot.TeleBot('6473154782:AAGcB7653icAtDh-Q66J41--C2ECmluxeu8')
# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")
# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов


class autocorrect(): 
                                                                                        
    def __init__(self):
        self.dictionary = {} # при вызове класса autocorrect() автоматически создатся пустой словарь для корректных слов

    def damerau_levenshtein_distance(self, a, b):
        ''' алгоритм или расстояние Левенштайна-демару является расстоянием Левенштайна, но с учетом транспощиций
        мы считаем сколько действий по редактированию одной строки надо сделать чтобы привести ее к виду другой строки
        при этом действий может быть всего 4: удаление символа, добавление и замена символа или транспозиция соседних символов.
        чтобы слово например фыв стало фыф, надо отредактировать 1 символ, такие слова мы и будем искать согласно заданию'''
        d = {} #создание словаря 
        lenstra = len(a)
        lenstrb = len(b)
        #создание двухмерного словаря для подсчета минимальных преобразований
        for i in range(-1,lenstra+1):
            d[(i,-1)] = i+1 #это берется из формулы расстояние Дамерау — Левенштейна
        for j in range(-1,lenstrb+1):
            d[(-1,j)] = j+1 #это берется из формулы расстояние Дамерау — Левенштейна
    
        for i in range(lenstra):
            for j in range(lenstrb):
                if a[i] == b[j]:  #сверяем каждую букву слова(ключа) со словом которым мы ввели
                    cost = 0        # если они равны, то преобразовывать ничего не надо и стоимость 0
                else:
                    cost = 1
                
                #заполняем наш двумерный словарь значениями, которые зависят от количества преобразований
                d[(i,j)] = min(
                            d[(i-1,j)] + 1, # удаление
                            d[(i,j-1)] + 1, # вставка
                            d[(i-1,j-1)] + cost, # замена
                            )
                
                # и если мы можем поменять местами необходимые нам буквы для получение нужного результата
                # то мы можем выполнить перестановку 
                if i and j and a[i] == b[j-1] and a[i-1] == b[j]: 
                    d[(i,j)] = min(d[(i,j)], d[i-2,j-2] + 1) # перестановка
    
        return d[lenstra-1,lenstrb-1] # после чего возвращаем последнее значение по ключу 
        

    def init_dict(self, new_word):
        self.dictionary[new_word.lower()] = None # записываем наше слово в словарь без значения, так как нам нужны только ключи

    def find_similar(self, word):#ищет в словаре наше вводимое слово в словаре
        word = word.lower()
        if word in self.dictionary:
            return True
        return False

    def correction(self, word):
        '''создает массив. рассматривает ключи и слова, после чего ссылается на функцию distance(где и есть наш алгоритм Левенштейна),
        которая считает сколько преобразований надо сделать чтобы превратить слово полученное на входе в слово которое 
        в словаре, если меньше или равно одному то слово нам подходит, добавляем его в массив а потом сортируем, так как
        может случится так что к нашему слову подойдут сразу несколько значений ключей и в задании попросили вывести их отсортированными''' 
        word = word.lower()
        correct = []
        for key in self.dictionary:                                 #забираем ключи 
            dist = self.damerau_levenshtein_distance(key, word)     #считаем сколько символов надо поменять чтобы получить словарное слово
            if dist <= 1:                                           #смотрим чтобы разница между ключом(словарным словом) и словом на вводе была в 1 символ
                correct.append(key)                                 #добавляем в массив наши ключи (правильные слова)
        correct.sort()
        return correct


Demaru = autocorrect()


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub(r'\([^()]*\)', '', wikitext2)
        wikitext2=re.sub(r'\([^()]*\)', '', wikitext2)
        wikitext2=re.sub(r'\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'К сожалению у меня отсутствует информация об этом'
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет,Меня зовут Кейсибот, отправьте мне название любой породы собак\nНапример: собака мопс\nИ я вам кратко расскажу о ней, так же, могу просто поболтать)')
@bot.message_handler(commands=["help"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне название любой породы собак\nНапример: собака мопс\nИ я вам кратко расскажу о ней, так же, могу просто поболтать)')

dict =["собака","приве", "здравствуй", "хай", "хело","здравствуйте","как дела", "как поживаешь","хорошо","как ты", "как твои дела","кто ты","ты кто","что ты делаешь", "как тебя зовут", "как твое имя", "имя","скажи имя","что делаешь","чем занимаешься","что сейчас делаешь","пока","досвидания","байбай","покеда"]
hello = ["приве", "здравствуй", "хай", "хело", "хелло","здравствуйте"]
kakdel = ["как дела", "как поживаешь","как ты","как твои дела"]
kto = ["кто ты","ты кто", "как тебя зовут", "как твое имя", "имя","скажи имя"]
chto = ["что делаешь","чем занимаешься","что сейчас делаешь", "что ты делаешь"]
poka = ["пока","досвидания","байбай","покеда"]
xorowo = ["хорошо"]
for i in dict:
    Demaru.init_dict(i)

pokaans = ["Пока, пока(","Пока(","Приходи еще, я буду скучать(","Заглядывай, я буду ждать)"]
kakdelans = ['хорошо!', 'чудесно!','лучше не бывает)','у меня все хорошо)','Супер!']
helloans = ['Привет, привет)', 'Здравствуй)','Привет)']
chtoans = ['Зависаю в интернете',"Сижу в тг","Читаю новости","Смотрю видео"]

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    mes = (message.text).lower()

    if mes.find("собака") != -1:
        mes = mes.replace('собака','')
        if "собак" in (getwiki(mes)):
            bot.send_message(message.chat.id, getwiki(mes))
            return None
        else:
            bot.send_message(message.chat.id, "Думаю, это не порода собаки")
            return None
    
    correct = Demaru.correction(mes)
    res = ', '.join(correct)
    mes = str(res) 
    print(mes)
    if mes in hello:
        bot.send_message(message.chat.id, helloans[random.randint(0,len(helloans))-1])
        return None
    if mes in kakdel:
        bot.send_message(message.chat.id, kakdelans[random.randint(0,len(kakdelans))-1])
        return None
    if mes in kto:
        bot.send_message(message.chat.id, "Меня зовут Кейсибот, я предоставляю информацию о всех породах собак, просто напиши мне 'собака' и породу собаки")
        return None
    if mes in chto:
         bot.send_message(message.chat.id, chtoans[random.randint(0,len(chtoans))-1])
         return None
    if mes in poka:
        bot.send_message(message.chat.id, pokaans[random.randint(0,len(pokaans))-1])
        return None
    if mes in xorowo:
        bot.send_message(message.chat.id, "Хорошо, что хорошо)")
    else:
        bot.send_message(message.chat.id, "К сожалению, не понимаю(")

# Запускаем бота
bot.polling(none_stop=True, interval=0)