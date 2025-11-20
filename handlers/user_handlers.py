from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.states import Registration
from keyboards.builders import get_contact_keyboard, get_program_keyboard
from database.db import add_lead, check_user_exists
from utils.sheets import send_to_sheets
from config import ALLOW_DUPLICATE_SUBMISSIONS
import os

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if not ALLOW_DUPLICATE_SUBMISSIONS:
        user_exists = await check_user_exists(message.from_user.id)
        if user_exists:
            await message.answer("Вы уже отправили заявку ранее. Спасибо за интерес!")
            return
    
    await state.set_state(Registration.waiting_for_phone)
    photo = FSInputFile(os.path.join("images", "start.png"))
    await message.answer_photo(
        photo=photo,
        caption="Здравствуйте! Пожалуйста, оставьте свои контактные данные, чтобы мы могли связаться с вами по вопросам обучения."
    )
    await message.answer(
        "Выберите способ отправки номера:",
        reply_markup=get_contact_keyboard()
    )

@router.message(Registration.waiting_for_phone, F.contact)
async def process_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Registration.waiting_for_program)
    await message.answer(
        "Какое направление вам интересно?",
        reply_markup=get_program_keyboard()
    )

@router.message(Registration.waiting_for_phone, F.text == "У меня другой номер")
async def process_manual_number_request(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_for_manual_phone)
    await message.answer(
        "Пожалуйста, введите ваш номер телефона:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Registration.waiting_for_manual_phone)
async def process_manual_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Registration.waiting_for_program)
    await message.answer(
        "Какое направление вам интересно?",
        reply_markup=get_program_keyboard()
    )

@router.callback_query(Registration.waiting_for_program)
async def process_program(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    callback_data = callback.data
    
    program_map = {
        "program_frontend": "FrontEnd",
        "program_backend": "BackEnd",
        "program_design": "Design",
        "program_gamedev": "GameDev",
        "program_pm": "Project Manager",
        "program_skip": ""
    }
    
    program = program_map.get(callback_data, "")
    
    data = await state.get_data()
    phone = data.get("phone")
    user = callback.from_user
    
    await add_lead(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        phone=phone,
        program=program
    )
    
    payload = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "phone": phone,
        "program": program
    }
    
    await send_to_sheets(payload)
    await state.clear()
    
    photo = FSInputFile(os.path.join("images", "done.png"))
    await callback.message.answer_photo(
        photo=photo,
        caption="Спасибо! Ваша заявка успешно отправлена.",
        reply_markup=ReplyKeyboardRemove()
    )

@router.callback_query()
async def inactive_button(callback: CallbackQuery):
    await callback.answer("Эта кнопка уже не активна :)", show_alert=False)
