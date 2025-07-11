#!/bin/bash

# Kiểm tra xem tiến trình đang chạy chưa
if ! pgrep -f "python.*main.py" > /dev/null; then
  # Nếu chưa chạy thì vào môi trường ảo rồi chạy
  source /home/zcsiaxcv/virtualenv/botzl2/3.11/bin/activate
  cd /home/zcsiaxcv/botzl2
  nohup python main.py > log.txt 2>&1 &
fi


