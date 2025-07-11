
from zlapi import ZaloAPI
from zlapi.models import *
import time
from concurrent.futures import ThreadPoolExecutor
import threading
import random
import os
des = {
    'version': "1.0.2",
    'credits': "LAMDev",
    'description': "Xử lý lệnh ping để kiểm tra độ trễ của BOT.",
}
def ping(message, message_object, thread_id, thread_type, author_id, self):
        start_time = time.time()
        reply_message = Message("Kiểm tra Ping, Độ trễ của BOT...")
        self.replyMessage(reply_message, message_object, thread_id, thread_type,ttl=60000)

        end_time = time.time()
        ping_time = end_time - start_time

        image_dir = "./gai"
        image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        random_image = random.choice(image_files)
        image_path = os.path.join(image_dir, random_image)

        text = f"🎾 Ping: độ trễ của BOT hiện tại là: {ping_time:.2f}ms"
        self.sendLocalImage(imagePath=image_path, thread_id=thread_id, thread_type=thread_type,ttl=60000, message=Message(text))

def get_tmii():
    return {
        'ping': ping
    }