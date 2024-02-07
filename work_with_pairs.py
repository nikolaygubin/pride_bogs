from create_bot import dp
from data_base import sqlite_db
from keyboards import inline_kb_impress, inline_kb_active
import difflib
import datetime
from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup
from handlers.admin import ID

def similarity(s1, s2):
  normalized1 = s1.lower()
  normalized2 = s2.lower()
  matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
  return matcher.ratio()

async def send_invoice_message(user_id, send_id, text):
    values = list(await sqlite_db.get_profile(user_id))
    age = datetime.datetime.now().year - int(values[11].split('.')[2])
    format = str()
    if values[10]:
        format = 'Онлайн'
    else :
        format = 'Оффлайн'
    card = f'{values[2]} из города {values[4]}\nВозраст: {age}\n\nTelegram: {values[1]}\nНомер телефона: {values[5]}\n\nСфера деятельности: {values[6]}\n\nИнтересы/Ресурсы/ Хобби: {values[8]}\n\nНазвание компании: {values[7]}\n\nЦель использования PRIDE CONNECT: {values[12]}\n\nФормат встречи: {format}\n\nОт встречи ожидает: {values[9]}'      
    try: 
        # pass
        inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text=f'Написать {values[2]}', url='https://t.me/' + values[1][1::]))
        await dp.bot.send_photo(send_id, photo=await sqlite_db.get_photo(user_id), caption=card, reply_markup=inline_keyboard)
        photo = open('./content/photo/right.jpeg', 'rb')
        await dp.bot.send_photo(send_id, photo=photo)
        await dp.bot.send_message(send_id, "Во время встречи оффлайн или онлайн не забудьте сделать фотографию с Вашим партнёром и отправить нашему администратору https://t.me/baribeshnik. Самые удачные мы будем опубликовывать в наших социальных сетях!")
    except:
        inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True).row(InlineKeyboardButton(text=f'Написать {values[2]}', url='https://t.me/' + values[1][1::]))
        await dp.bot.send_message(send_id, text=card, reply_markup=inline_keyboard)
        photo = open('./content/photo/right.jpeg', 'rb')
        await dp.bot.send_photo(send_id, photo=photo)
        print('Я в блоке')
    
async def make_pairs():
        await sqlite_db.check_block()
        await sqlite_db.clear_temp_users()
        await sqlite_db.delete_current_pairs()
        offline_users = await sqlite_db.get_offline_users() # получаем всех оффлайн пользователей (id + town)
        online_users = await sqlite_db.get_online_users() # получаем всех онлайн пользователей (только id)
        dict_pairs = dict(str()) # словарь со всеми парами

        print(offline_users)
        print(online_users)

        offline_dict = {} # инициализируем словарь и заносим туда всех оффлайн пользователей по городам
        for user in offline_users: 
            town = user[1].lower()
            if offline_dict.get(town) == None:
                offline_dict[town] = list()
            offline_dict[town].append(user[0])


        for town in offline_dict.keys():
            town_users = list(offline_dict[town])
            
            for user_id in town_users:
                left_user = user_id
                for i in range(len(town_users)):
                    if town_users[i] == left_user:
                        continue
                    
                    if not await sqlite_db.is_last_pair(left_user, town_users[i]):
                        dict_pairs[left_user] = town_users[i]
                        await sqlite_db.append_pair(left_user, town_users[i]) # добавляем пары в базу данных
                        offline_dict[town].remove(town_users[i])
                        offline_dict[town].remove(left_user)
                        # town_users.remove(left_user)
                        # town_users.remove(town_users[i])
                        break
                        
        offline_size = len(dict_pairs)
        
        online_id = list() # создаём список и добавляем туда все онлайн id
        for town in offline_dict.keys():
            users = offline_dict[town]
            for user in users:
                online_id.append(user)

        for user in online_users:
            online_id.append(user[0])

        print(online_id)

        for user_id in online_id:
            left_user = user_id
            for i in range(len(online_id)):
                if online_id[i] == left_user:
                    continue
                
                if not await sqlite_db.is_last_pair(left_user, online_id[i]):
                    dict_pairs[left_user] = online_id[i]
                    await sqlite_db.append_pair(left_user, online_id[i]) # добавляем пары в базу данных
                    # online_users.remove(left_user)
                    # online_users.remove(online_users[i])
                    break

        count = 0
        for key, value in dict_pairs.items():
            if count < offline_size:
                await send_invoice_message(key, value, 'Поздравляем! Вам нашлась оффлайн пара, советуем договориться о встрече сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
                await send_invoice_message(value, key, 'Поздравляем! Вам нашлась оффлайн пара, советуем договориться о встрече сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
            else:
                await send_invoice_message(key, value, 'Поздравляем! Вам нашлась онлайн пара, советуем написать сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
                await send_invoice_message(value, key, 'Поздравляем! Вам нашлась онлайн пара, советуем написать сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
            count += 1

        await dp.bot.send_message(ID[0], f'Подобрано {len(dict_pairs)} пар, из них {offline_size} оффлайн и {len(dict_pairs) - offline_size} онлайн пар!\n\
Не доставлось пары {(len(offline_users) + len(online_users)) - len(dict_pairs) * 2} пользователям.')

        return len(dict_pairs)

        # for town in offline_dict.keys(): # проходимся по всем городам и пытаемся сформировать пары
        #     town_id = list(offline_dict[town]) # иницализируем массив с пользователями в городе town
        #     for id in range(len(town_id)): # пытаемся подобрать пару каждому пользователю
        #         max_sim = -1    
        #         max_index = id  # индекс с максимальной схожестью (по умолчанию ссылается на самого себя)
        #         for pair_id in range(len(town_id)):
        #             if town_id[id] in dict_pairs.values():
        #                 break
        #             if id == pair_id or town_id[pair_id] in dict_pairs.keys() or town_id[pair_id] in dict_pairs.values() or await sqlite_db.is_last_pair(town_id[id], town_id[pair_id]):
        #                 continue   
        #             s1 = await sqlite_db.get_hooks(town_id[id])
        #             s2 = await sqlite_db.get_hooks(town_id[pair_id])
        #             sim = similarity(s1, s2) # процент схожести 2 строк 
        #             if sim > max_sim:
        #                 max_index = pair_id
        #                 max_sim = sim
        #         if max_index != id:
        #             dict_pairs[town_id[id]] = town_id[max_index]
        #             await sqlite_db.append_pair(town_id[id], town_id[max_index]) # добавляем пары в базу данных
        #             offline_dict[town].remove(town_id[id])
        #             offline_dict[town].remove(town_id[max_index])

        # offline_size = len(dict_pairs)

        # online_id = list() # создаём список и добавляем туда все онлайн id
        # for town in offline_dict.keys():
        #     users = offline_dict[town]
        #     for user in users:
        #         online_id.append(user)

        # for user in online_users:
        #     online_id.append(user[0])

        # for id in range(len(online_id)):
        #     max_sim = -1
        #     max_index = id
        #     for pair_id in range(len(online_id)):
        #         if online_id[id] in dict_pairs.values():
        #             break
        #         if id == pair_id or online_id[pair_id] in dict_pairs.keys() or online_id[pair_id] in dict_pairs.values() or await sqlite_db.is_last_pair(online_id[id], online_id[pair_id]):
        #             continue     
        #         s1 = await sqlite_db.get_hooks(online_id[id])
        #         s2 = await sqlite_db.get_hooks(online_id[pair_id])
        #         sim = similarity(s1, s2)
        #         if sim > max_sim:
        #             max_index = pair_id
        #             max_sim = sim
        #     if max_index != id:
        #         dict_pairs[online_id[id]] = online_id[max_index]
        #         await sqlite_db.append_pair(online_id[id], online_id[max_index])

#         count = 0
#         for key, value in dict_pairs.items():
#             if count < offline_size:
#                 await send_invoice_message(key, value, 'Поздравляем! Вам нашлась оффлайн пара, советуем договориться о встрече сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
#                 await send_invoice_message(value, key, 'Поздравляем! Вам нашлась оффлайн пара, советуем договориться о встрече сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
#             else:
#                 await send_invoice_message(key, value, 'Поздравляем! Вам нашлась онлайн пара, советуем написать сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
#                 await send_invoice_message(value, key, 'Поздравляем! Вам нашлась онлайн пара, советуем написать сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
#             count += 1

#         await dp.bot.send_message(ID[0], f'Подобрано {len(dict_pairs)} пар, из них {offline_size} оффлайн и {len(dict_pairs) - offline_size} онлайн пар!\n\
# Не доставлось пары {(len(offline_users) + len(online_users)) - len(dict_pairs) * 2} пользователям.')
            
#         if len(dict_pairs) * 2 != len(offline_users) + len(online_users):
#             await sqlite_db.find_users_without_pair()
            
#         return len(dict_pairs)

    # except Exception:
    #     await dp.bot.send_message(555581588, 'Возникла ошибка при подборе пар')
async def ask_impress():
    users = await sqlite_db.get_users()
    if len(users) == 0:
        return
    count = 0
    for user in users:
        counter = 0
        for pair in reversed(user[1]):
            if user[2][-1 - counter] == 0:
                pair_user = await sqlite_db.get_profile(pair)
                try:
                    await dp.bot.send_message(user[0], f'Как прошла встреча с {pair_user[2]} из города {pair_user[4]}?\nTg : {pair_user[1]}', reply_markup=inline_kb_impress)
                    count += 1
                except:
                    pass
            counter += 1
    return count
            
async def make_extra_pairs():
    users = await sqlite_db.get_extra_users()
    dict_pairs = dict(str())
    for id in range(len(users)):
        max_sim = -1
        max_index = id
        for pair_id in range(len(users)):
            if users[id] in dict_pairs.values():
                break
            if id == pair_id or users[pair_id] in dict_pairs.keys() or users[pair_id] in dict_pairs.values() or await sqlite_db.is_last_pair(users[id], users[pair_id]):
                continue     
            s1 = await sqlite_db.get_hooks(users[id])
            s2 = await sqlite_db.get_hooks(users[pair_id])
            sim = similarity(s1, s2)
            if sim > max_sim:
                max_index = pair_id
                max_sim = sim
        if max_index != id:
            dict_pairs[users[id]] = users[max_index]
            await sqlite_db.append_pair(users[id], users[max_index])
    for key, value in dict_pairs.items():
        await send_invoice_message(key, value, 'Поздравляем! Вам нашлась дополнительная пара, советуем написать сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
        await send_invoice_message(value, key, 'Поздравляем! Вам нашлась дополнительная пара, советуем написать сразу, приятного общения🤝\nВы можете начать знакомство с этой фразы : «Привет! Я из приложения PRIDE CONNECT) Ты мой собеседник на этой неделе\n\n У тебя как по времени на неделе? Давай созвонимся / встретимся?»')
        await sqlite_db.delete_from_temp_users(key)
        await sqlite_db.delete_from_temp_users(value)
    
    return len(dict_pairs)
    
    
async def is_active():
    users = await sqlite_db.get_users_for_is_active()
    counter = 0
    for user in users:
        try:
            await dp.bot.send_message(user, 'Новая неделя - новые знакомства!\nИскать вам пару на следующую неделю?', reply_markup=inline_kb_active)
            counter += 1
        except:
            print('Я в блоке')
            
    return counter

async def update_paid():
    await sqlite_db.update()
    
async def del_promo():
    await sqlite_db.del_out_promo();