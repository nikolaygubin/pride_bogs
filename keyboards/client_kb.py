from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

inl_button1 = InlineKeyboardButton(text='Назад', callback_data='back_mes')
inl_button2 = InlineKeyboardButton(text='Верно ✅', callback_data='right')
inl_button3 = InlineKeyboardButton(text='Заполнить заново', callback_data='fill_again')
                                                    
inl_menuchange_button1 = InlineKeyboardButton(text='Имя', callback_data='change_name')
inl_menuchange_button2 = InlineKeyboardButton(text='Фото', callback_data='change_photo')
inl_menuchange_button3 = InlineKeyboardButton(text='Город', callback_data='change_town')
inl_menuchange_button4 = InlineKeyboardButton(text='Социальные сети', callback_data='change_social_network')
inl_menuchange_button5 = InlineKeyboardButton(text='Занятия/работа', callback_data='change_work')
inl_menuchange_button6 = InlineKeyboardButton(text='Хобби/увлечения', callback_data='change_hobby')
inl_menuchange_button7 = InlineKeyboardButton(text='Формат встреч', callback_data='change_format')
inl_menuchange_button8 = InlineKeyboardButton(text='Ожидания', callback_data='change_expect')
inl_menuchange_button9 = InlineKeyboardButton(text='Возраст', callback_data='change_data')
inl_menuchange_button10 = InlineKeyboardButton(text='Цель', callback_data='change_purpose')
inl_menuchange_button11 = InlineKeyboardButton(text='E-mail', callback_data='change_email')
inl_menuchange_button12 = InlineKeyboardButton(text='Выход', callback_data='change_exit')

kb_menuchange = InlineKeyboardMarkup(resize_keyboard=True).add(inl_menuchange_button1).add(inl_menuchange_button2).add(inl_menuchange_button3)\
                                                          .add(inl_menuchange_button4).add(inl_menuchange_button5).add(inl_menuchange_button6)\
                                                          .add(inl_menuchange_button7).add(inl_menuchange_button8).add(inl_menuchange_button9)\
                                                          .add(inl_menuchange_button10).add(inl_menuchange_button11).add(inl_menuchange_button12)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Заполнить_анкету'), KeyboardButton('Оплатить_подписку'))

inline_kb_quest = InlineKeyboardMarkup(resize_keyboard=True).row(inl_button1)
inline_kb_quest_social = InlineKeyboardMarkup(resize_keyboard=True).row(inl_button1)
inline_kb_quest_format = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Вживую', callback_data='offline'),\
InlineKeyboardButton(text='Онлайн', callback_data='online')).row(inl_button1)

inline_kb_change_format = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Вживую', callback_data='offline'),\
InlineKeyboardButton(text='Онлайн', callback_data='online')).row(inl_button1)

inline_kb_verify = InlineKeyboardMarkup(resize_keyboard=True).row(inl_button2).row(inl_button3)
inline_kb_succses = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Понятно, дальше ⏩', callback_data='succses')).row(inl_button3)

promo_button = InlineKeyboardButton(text='Есть промокод🌟', callback_data='promocode')

menu_promo_button = InlineKeyboardButton(text='Есть промокод🌟', callback_data='menu_promocode')

inline_kb_buy = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Оплатить месяц💵', callback_data='buy_month'))\
                                                          .row(InlineKeyboardButton(text='Оплатить год💵', callback_data='buy_year'))\
                                                          .row(InlineKeyboardButton(text='Активировать промокод🌟', callback_data='just_promo'))\
                                                          .row(InlineKeyboardButton(text='Оплатить позднее🔜', callback_data='buy_later'))
                                                          
inline_promo = InlineKeyboardMarkup(resize_keyboard=True).row(promo_button)\
                                                         .row(InlineKeyboardButton(text='Оплатить сразу', callback_data='buy_now'))\
                                                         .row(inl_button1)

inline_kb_menu_buy = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Оплатить месяц💵', callback_data='menu_buy_month'))\
                                                               .row(InlineKeyboardButton(text='Оплатить год💵', callback_data='menu_buy_year'))\
                                                               .row(InlineKeyboardButton(text='Назад🔙', callback_data='back_main'))

inline_menu_promo = InlineKeyboardMarkup(resize_keyboard=True).row(menu_promo_button)\
                                                         .row(InlineKeyboardButton(text='Оплатить сразу', callback_data='buy_now_menu'))\
                                                         .row(InlineKeyboardButton(text='Назад🔙', callback_data='menu_back'))


inline_kb_buy_only = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Оплатить', callback_data='buy'))\
                                                               .row(InlineKeyboardButton(text='Оплатить позднее🔜', callback_data='buy_later'))

inline_kb_go = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Поехали 🚀', callback_data='next'))

inline_kb_menu = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Мой профиль📔', callback_data='show_profile'), InlineKeyboardButton(text='Редактировать✏️', callback_data='change_profile'))\
                                                            .row(InlineKeyboardButton(text='Моя подписка✔️', callback_data='check_paid'), InlineKeyboardButton(text='Оплатить💵', callback_data='buy_sub'))\
                                                            .row(InlineKeyboardButton(text='Текущая пара💬', callback_data='current_buddy'), InlineKeyboardButton(text='Новая пара🆕', callback_data='get_new_buddy'))\
                                                            .row(InlineKeyboardButton(text='История встреч🤝', callback_data='get_history'))

inline_kb_back_menu = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Назад🔙', callback_data='back_main'))

inline_kb_impress = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Отлично✅', callback_data='nice'),
                                                                   InlineKeyboardButton(text='Не понравилось🙅‍♂️', callback_data='bad')).row(
                                                                   InlineKeyboardButton(text='Пока не встретились🔜', callback_data='not_meet'))
                                                                   
                                                        
inline_kb_active = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Конечно✅', callback_data='active_user'),
                                                                   InlineKeyboardButton(text='Пропущу неделю🔜', callback_data='skip_week'))

inline_kb_expect = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='100% польза', callback_data='100% польза')).row(
                                                                   InlineKeyboardButton(text='70% польза - 30% фан', callback_data='70% польза - 30% фан')).row(
                                                                   InlineKeyboardButton(text='50% польза - 50% фан', callback_data='50% польза - 50% фан')).row(
                                                                   InlineKeyboardButton(text='30% польза - 70% фан', callback_data='30% польза - 70% фан')).row(
                                                                   InlineKeyboardButton(text='100% фан', callback_data='100% фан')).row(inl_button1)
                                                                   
thx_next = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Спасибо, поехали дальше✅', callback_data='thx_next'))

accept_photo = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Хорошо, далее✅', callback_data='accept')).row(
                                                             InlineKeyboardButton(text='Хочу отправить другую фотографию!', callback_data='other'))

kb_purpose = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text=' ⁃ Найти новые связи для решения задач по проектам', callback_data='1_purpose')).row(
                                                            InlineKeyboardButton(text=' ⁃ Создать коллаборации и партнерства', callback_data='2_purpose')).row(
                                                            InlineKeyboardButton(text=' ⁃ Найти подрядчиков в разных нишах', callback_data='3_purpose')).row(
                                                            InlineKeyboardButton(text=' ⁃ Познакомиться с интересными людьми', callback_data='4_purpose')).row(
                                                            InlineKeyboardButton(text=' ⁃ Расширить свои возможности', callback_data='5_purpose')).row(inl_button1)
                                                            
kb_gender = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Мужчина', callback_data='male')).row(
                                                           InlineKeyboardButton(text='Женщина', callback_data='female')).row(inl_button1)      

kb_username = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Проверить username', callback_data='check_username'))  

kb_back_change = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text='Назад', callback_data='back_mes'))             

kb_history = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Вперёд➡️', callback_data='next_history'))\
                                                       .add(InlineKeyboardButton(text='Назад⬅️', callback_data='prev_history'))\
                                                       .row(InlineKeyboardButton(text='Выход🔙', callback_data='back_main'))
                                                       
kb_only_prev = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Назад⬅️', callback_data='prev_history'))\
                                                         .row(InlineKeyboardButton(text='Выход🔙', callback_data='back_main'))
kb_only_next = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Вперёд➡️', callback_data='next_history'))\
                                                         .row(InlineKeyboardButton(text='Выход🔙', callback_data='back_main'))