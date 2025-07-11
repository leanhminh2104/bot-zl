
import json
import os
from config import PREFIX
from zlapi.models import *
import random

users = {} 
DATA_FILE = "data/users.json"
des = {
    "version": "1.0.0",
    "credits": "Soiz",
    "description": "Tài Xỉu",
}

def load_data():
    """Tải dữ liệu người dùng từ file JSON."""
    global users
    try:
        with open(DATA_FILE, "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        save_data()

def save_data():
    """Lưu dữ liệu người dùng vào file JSON."""
    global users
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def handle_dangky(message, message_object, thread_id, thread_type, author_id, client):
    """Xử lý lệnh {PREFIX}dangky (đăng ký người dùng)."""
    global users
    username = message[len(PREFIX) + 7:].strip()
    if username:
        if author_id not in users:
            users[author_id] = {"username": username, "balance": 100000000}
            response = f"Đăng ký thành công! {username} đã nhận 100 triệu."
            save_data()
        else:
            response = "Bạn đã đăng ký rồi."
    else:
        response = "Vui lòng cung cấp tên đăng ký."
    client.replyMessage(Message(text=response),message_object, thread_id, thread_type)

def handle_sodu(message, message_object, thread_id, thread_type, author_id, client):
    """Xử lý lệnh {PREFIX}sodu (kiểm tra số dư)."""
    global users
    if author_id in users:
        balance = users[author_id]["balance"]
        response = f"Số dư hiện tại của bạn là: {balance}"
    else:
        response = f"Bạn chưa đăng ký. Vui lòng đăng ký bằng cách dùng lệnh {PREFIX}dangky (tên)."
    client.replyMessage(Message(text=response),message_object, thread_id, thread_type)

def handle_tx(message, message_object, thread_id, thread_type, author_id, client):
    """Xử lý lệnh {PREFIX}tx (chơi tài xỉu)."""
    global users
    response = ""
    try:
        parts = message.split()
        choice = parts[1]
        amount = int(parts[2])

        if author_id not in users:
            response = "Bạn chưa đăng ký. Vui lòng đăng ký bằng cách dùng lệnh dangky (tên)."
        elif choice not in ["tài", "xỉu"]:
            response = "Lựa chọn không hợp lệ. Vui lòng chọn 'tài' hoặc 'xỉu'."
        elif amount <= 0:
            response = "Số tiền phải lớn hơn 0."
        elif amount > users[author_id]["balance"]:
            response = "Số dư không đủ."
        else:
            outcome = random.choice(["tài", "xỉu"])
            if outcome == choice:
                users[author_id]["balance"] += amount
                response = f"Kết quả là {outcome}. Bạn đã thắng {amount}."
            else:
                users[author_id]["balance"] -= amount
                response = f"Kết quả là {outcome}. Bạn đã thua {amount}."
            
            sendmess = f"{response}"
            message_to_send = Message(text=sendmess)
            image_folder = f"data/{outcome}"
            image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
            if image_files:
                random_image = random.choice(image_files)
                image_path = os.path.join(image_folder, random_image)
                client.sendLocalImage(
                    image_path,
                    message=message_to_send,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=1600,
                    height=1600
                )
    except (IndexError, ValueError):
        response = f"Sai cú pháp. Vui lòng dùng lệnh {PREFIX}tx (tài/xỉu) (số tiền)."
    
    # client.sendMessage(Message(text=response), thread_id, thread_type)
    save_data()

def get_tmii():
    """Trả về danh sách các lệnh được hỗ trợ."""
    return {
        "tx": handle_tx,
        "dangky": handle_dangky,
        "sodu": handle_sodu,
    }

load_data()
