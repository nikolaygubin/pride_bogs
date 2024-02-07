from create_bot import dp, bot, storage
from aiogram import types, Dispatcher
from data_base import sqlite_db
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import kb_client
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from work_with_pairs import *
# from work_with_pairs import make_pairs
import work_with_pairs
from aiogram.dispatcher.webhook import SendMessage

ID = [555581588, 261295913, 5446068361, 2137624598,1327107969]
                
inline_kb_panel = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Статистика', callback_data='statistics')).add(
                InlineKeyboardButton(text='Действия', callback_data='actives')).add(
                # InlineKeyboardButton(text='Промокоды', callback_data='promocodes')).add(
                InlineKeyboardButton(text='Выход', callback_data='close'))       
                
inline_kb_statistics = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Количество пользователей', callback_data='count_users')).add(
                InlineKeyboardButton(text='Количество по городам', callback_data='count_users_town')).add(
                InlineKeyboardButton(text='Кол-во активных пользователей', callback_data='active_users')).add(
                InlineKeyboardButton(text='Назад', callback_data='back_admin_main'))  
                
inline_kb_actions = InlineKeyboardMarkup(resize_keyboard=True).add(
                InlineKeyboardButton(text='Отправить сообщение всем', callback_data='send_message')).add(
                InlineKeyboardButton(text='Подобрать пары всем', callback_data='make_pairs')).add(
                InlineKeyboardButton(text='Опросить всех на активность', callback_data='ask_active')).add(
                InlineKeyboardButton(text='Опрос впечатлений от встречи', callback_data='ask_impress_admin')).add(
                InlineKeyboardButton(text='Назад', callback_data='back_admin_main'))
                # InlineKeyboardButton(text='Подобрать extra пары', callback_data='make_extra_pairs')).add(
                # InlineKeyboardButton(text='Пересмотреть подписки', callback_data='see_active')).add(
                
# inline_kb_promo = InlineKeyboardMarkup(resize_keyboard=True).add(
#                 InlineKeyboardButton(text='Показать промокоды', callback_data='show_promo')).add(
#                 InlineKeyboardButton(text='Добавить промокод', callback_data='add_promo')).add(
#                 InlineKeyboardButton(text='Удалить промокод', callback_data='del_promo')).add(
#                 InlineKeyboardButton(text='Назад', callback_data='back_admin_main'))  
                
inline_kb_back_stat = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Назад', callback_data='back_stat'))  
inline_kb_back_act = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Назад', callback_data='back_act')) 
# inline_kb_back_promo = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Назад', callback_data='back_promo'))        

class Admin(StatesGroup):
    start = State()
    statistics = State()
    stat_point = State()
    
    actions = State()
    action_point = State()
    # del_promo = State()
    
    # promocodes = State()
    # promo_point = State()


async def admin_panel(message : types.Message, state : FSMContext):    
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['State'] = await state.get_state()
            # data['State'] = dp.get_current().current_state()
            # if data.get('Admin_message') != None:
            #     msg = types.Message.to_object(data['Admin_message'])
            #     await msg.delete()
            msg = await message.answer('Админ панель', reply_markup=inline_kb_panel)
            data['Admin_message'] = msg.to_python()
        await Admin.start.set()
    await message.delete()
    
    
async def close_admin_panel(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        await state.set_state(data['State'])
        msg = types.Message.to_object(data['Admin_message'])
        await msg.delete()
    # await state.finish()

async def back_main(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Админ панель', reply_markup=inline_kb_panel)
    await Admin.start.set()

async def statistics_menu(callback_query : types.callback_query, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Статистика', reply_markup=inline_kb_statistics)
    await Admin.statistics.set()
    
async def count_users(callback_query : types.callback_query, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text(f'Количество пользователей = {await sqlite_db.count()}', reply_markup=inline_kb_back_stat)
    await Admin.stat_point.set()
    
async def count_users_town(callback_query : types.callback_query, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text(f'Пользователи по городам:\n{await sqlite_db.count_for_town()}', reply_markup=inline_kb_back_stat)
    await Admin.stat_point.set()    
    
# async def paid_users(callback_query : types.callback_query, state : FSMContext):
#     await callback_query.answer()
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message'])
#         await msg.edit_text(f'Платных подписок = {await sqlite_db.count_paid_subs()}', reply_markup=inline_kb_back_stat)
#     await Admin.stat_point.set()  

# async def demo_users(callback_query : types.callback_query, state : FSMContext):
#     await callback_query.answer()
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message'])
#         await msg.edit_text(f'Демо подписок = {await sqlite_db.count_demo_subs()}', reply_markup=inline_kb_back_stat)
#     await Admin.stat_point.set()  
    
async def active_users(callback_query : types.callback_query, state : FSMContext):
    await callback_query.answer()        
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text(f'Активных на этой неделе = {await sqlite_db.active_users()}', reply_markup=inline_kb_back_stat)
    await Admin.stat_point.set() 

# async def see_ref(callback_query : types.callback_query, state : FSMContext):
#     await callback_query.answer()        
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message'])
#         await msg.edit_text(f'{await sqlite_db.get_refs()}', reply_markup=inline_kb_back_stat)
#     await Admin.stat_point.set() 

 
    
async def back_stat(callback_query : types.callback_query, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Статистика', reply_markup=inline_kb_statistics)
    await Admin.statistics.set()
    
async def actions_menu(callback_query : types.callback_query, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Действия', reply_markup=inline_kb_actions)
    await Admin.actions.set()
    
async def make_pairs_admin(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        try:
            await msg.edit_text('Подбираем пары...')
        except:
            pass
        count = await work_with_pairs.make_pairs()
        await msg.edit_text(f'Успешно получилось подобрать {count} пар!', reply_markup=inline_kb_actions)
        
async def make_extra_pairs_admin(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        try:
            await msg.edit_text('Подбираем пары...')
        except:
            pass
        count = await work_with_pairs.make_extra_pairs()
        await msg.edit_text(f'Успешно получилось подобрать {count} пар!', reply_markup=inline_kb_actions)
        
# async def see_paid(callback_query : types.CallbackQuery, state : FSMContext):
#     await callback_query.answer()
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message'])
#         try:
#             await msg.edit_text('Проверяем подписку...')
#         except:
#             pass
#         count = await sqlite_db.update()
#         await msg.edit_text(f'Найдено и обнулено {count} просроченных подписок!', reply_markup=inline_kb_actions)
        
async def ask_active(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        try:
            await msg.edit_text('Опрашиваем на активность...')
        except:
            pass
        count = await work_with_pairs.is_active()
        await msg.edit_text(f'Удалось опросить {count} пользователей!', reply_markup=inline_kb_actions)
        
async def ask_impress_admin(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Оправшиваем о впечатлениях...')
        count = await work_with_pairs.ask_impress()
        await msg.edit_text(f'Опрос о впечатлениях удалось отправить {count} пользователям!', reply_markup=inline_kb_actions)
        
async def send_message(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Напишите сообщение, которое хотите отправить всем пользователям', reply_markup=inline_kb_back_act)
    await Admin.action_point.set()

async def get_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        await message.delete()
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Отправляем сообщения...')
        count = await sqlite_db.send_message(message)
        await msg.edit_text(f'Ваше сообщение успешно доставлено {count} пользователям', reply_markup=inline_kb_actions)   
    await Admin.actions.set() 

async def back_act(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Действия', reply_markup=inline_kb_actions)
    await Admin.actions.set()
        
# async def promocodes_menu(callback_query : types.CallbackQuery, state : FSMContext):
#     await callback_query.answer()
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message'])
#         await msg.edit_text('Промокоды', reply_markup=inline_kb_promo)

# async def show_promo(callback_query : types.CallbackQuery, state : FSMContext) :
#     await callback_query.answer() 
#     all_promo = await sqlite_db.get_promocodes() 
#     str_promo = 'Промокоды :\n'
#     for promo in all_promo :
#         str_promo += f'{promo[0]}  {promo[1]}% {promo[2]} активаций (до {promo[4]})\n'
#     await Admin.promo_point.set()

#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message']) 
#         await msg.edit_text(str_promo, reply_markup=inline_kb_back_promo)
     
# async def add_promo(callback_query : types.CallbackQuery, state : FSMContext):
#     await callback_query.answer() 
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message']) 
#         await msg.edit_text('Введите промокод в следующем формате : промокод - процент - количество активаций - количество месяцев\nПример: month 10 20 3\nПромкод с процентом 100 означает бесплатную подписку при его вводе', reply_markup=inline_kb_back_promo)
#     await Admin.promo_point.set()
    
# async def get_promo(message : types.Message, state : FSMContext):
#     return_str = await sqlite_db.insert_promo(message)
#     await message.delete()
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message'])
#         await msg.edit_text(return_str, reply_markup=inline_kb_promo)
#     await Admin.promocodes.set()
    
   
# async def back_promo(callback_query : types.CallbackQuery, state : FSMContext):
#     await callback_query.answer() 
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message'])
#         await msg.edit_text('Промокоды', reply_markup=inline_kb_promo)
    
async def actions_menu(callback_query : types.CallbackQuery, state : FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        msg = types.Message.to_object(data['Admin_message'])
        await msg.edit_text('Действия', reply_markup=inline_kb_actions)
    await Admin.actions.set()
    
# async def del_promo(callback_query : types.CallbackQuery, state : FSMContext):
#     await callback_query.answer()
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message']) 
#         await msg.edit_text('Введите название удаляемого промокода!', reply_markup=inline_kb_back_promo)
#     await Admin.del_promo.set()
    
# async def get_del_promo(message : types.Message, state : FSMContext):
#     return_str = await sqlite_db.remove_promo(message)
#     await message.delete()
#     async with state.proxy() as data:
#         msg = types.Message.to_object(data['Admin_message'])
#         await msg.edit_text(return_str, reply_markup=inline_kb_promo)
#     await Admin.promocodes.set()    
    
     
        
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(admin_panel, Text(equals='/admin', ignore_case=True), state='*') # main panel
    
    dp.register_callback_query_handler(statistics_menu, Text(equals='statistics', ignore_case=True), state=Admin.start) # statistics_menu
    dp.register_callback_query_handler(back_stat, Text(equals='back_stat', ignore_case=True), state=Admin.stat_point)  
    dp.register_callback_query_handler(count_users, Text(equals='count_users', ignore_case=True), state=Admin.statistics)
    dp.register_callback_query_handler(count_users_town, Text(equals='count_users_town', ignore_case=True), state=Admin.statistics)
    # dp.register_callback_query_handler(paid_users, Text(equals='paid_users', ignore_case=True), state=Admin.statistics)
    # dp.register_callback_query_handler(demo_users, Text(equals='demo_users', ignore_case=True), state=Admin.statistics)
    dp.register_callback_query_handler(active_users, Text(equals='active_users', ignore_case=True), state=Admin.statistics) 
    # dp.register_callback_query_handler(see_ref, Text(equals='refs', ignore_case=True), state=Admin.statistics)    
    
    dp.register_callback_query_handler(actions_menu, Text(equals='actives', ignore_case=True), state=Admin.start) # actions_menu
    dp.register_callback_query_handler(back_act, Text(equals='back_act', ignore_case=True), state=Admin.action_point)
    dp.register_callback_query_handler(send_message, Text(equals='send_message', ignore_case=True), state='*')
    dp.register_callback_query_handler(ask_active, Text(equals='ask_active', ignore_case=True), state='*')
    dp.register_callback_query_handler(make_pairs_admin, Text(equals='make_pairs', ignore_case=True), state='*')
    dp.register_callback_query_handler(make_extra_pairs_admin, Text(equals='make_extra_pairs', ignore_case=True), state='*')
    # dp.register_callback_query_handler(see_paid, Text(equals='see_active', ignore_case=True), state='*')
    dp.register_callback_query_handler(ask_impress_admin, Text(equals='ask_impress_admin', ignore_case=True), state='*')
    dp.register_message_handler(get_message, state=Admin.action_point)

    
    # dp.register_callback_query_handler(promocodes_menu, Text(equals='promocodes', ignore_case=True), state=Admin.start) # promo_menu
    # dp.register_callback_query_handler(show_promo, Text(equals='show_promo', ignore_case=True), state='*')
    # dp.register_callback_query_handler(add_promo, Text(equals='add_promo', ignore_case=True), state='*')
    # dp.register_message_handler(get_promo, state=Admin.promo_point)
    # dp.register_callback_query_handler(del_promo, Text(equals='del_promo', ignore_case=True), state='*')
    # dp.register_message_handler(get_del_promo, state=Admin.del_promo)
    # dp.register_callback_query_handler(back_promo, Text(equals='back_promo', ignore_case=True), state='*')
    
    
    
    dp.register_callback_query_handler(back_main, Text(equals='back_admin_main', ignore_case=True), state='*')
    dp.register_callback_query_handler(close_admin_panel, Text(equals='close', ignore_case=True), state=Admin.start) # close
    
    
