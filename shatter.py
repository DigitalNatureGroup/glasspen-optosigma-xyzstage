import serial
import time

# COMポート設定（例: COM4）
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)  # 接続安定のため少し待機

# 表示ラベル → 実際に送るコマンドの対応
LABEL_TO_SIGNAL = {
    "OPEN": "LOW",   # 開く = 低レベル
    "CLOSE": "HIGH", # 閉じる = 高レベル
}

def send_command(label: str):
    """操作ラベル（OPEN/CLOSE）でArduinoへ送信"""
    normalized_label = label.strip().upper()
    if normalized_label not in LABEL_TO_SIGNAL:
        raise ValueError("OPEN または CLOSE を指定してください。")

    actual_cmd = LABEL_TO_SIGNAL[normalized_label]
    ser.write((actual_cmd + '\n').encode('utf-8'))
    time.sleep(0.1)
    response = ser.readline().decode('utf-8', errors='ignore').strip()
    print(f"送信: {normalized_label}（実信号: {actual_cmd}）")
    print(f"Arduino: {response}")

try:
    while True:
        # 操作用のラベルで案内（送る信号は従来のLOW/HIGH）
        cmd_label = input("入力 (OPEN=LOW / CLOSE=HIGH / EXIT): ").strip().upper()
        if cmd_label == "EXIT":
            break

        if cmd_label in LABEL_TO_SIGNAL:
            send_command(cmd_label)
        elif cmd_label in ("HIGH", "LOW"):
            ser.write((cmd_label + '\n').encode('utf-8'))
            time.sleep(0.1)
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"送信: {cmd_label}")
            print(f"Arduino: {response}")
        else:
            print("⚠️ 'OPEN' / 'CLOSE' / 'HIGH' / 'LOW' / 'EXIT' を入力してください。")

except KeyboardInterrupt:
    pass
finally:
    ser.close()
    print("Serial切断完了")
