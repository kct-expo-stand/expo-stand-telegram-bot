from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.states import Registration
from keyboards.builders import get_contact_keyboard, get_skip_keyboard
from database.db import add_lead
from utils.sheets import send_to_sheets
import os

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_for_phone)
    photo = FSInputFile(os.path.join("images", "violet-genius.png"))
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
        reply_markup=get_skip_keyboard()
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
        reply_markup=get_skip_keyboard()
    )

@router.message(Registration.waiting_for_program)
async def process_program(message: Message, state: FSMContext):
    program = message.text
    if program.lower() == "пропустить":
        program = ""
    
    data = await state.get_data()
    phone = data.get("phone")
    user = message.from_user
    
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
    
    photo = FSInputFile(os.path.join("images", "violet-genius.png"))
    await message.answer_photo(
        photo=photo,
        caption="Спасибо! Ваша заявка успешно отправлена.",
        reply_markup=ReplyKeyboardRemove()
    )
