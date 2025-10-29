#!/usr/bin/env python3
"""
3軸ステージ制御テストプログラム
X, Y, Z軸を順番に動かす簡単なテスト
"""

import time

from pyOptoSigma.pyOptoSigma import Controllers, Session, Stages
import serial


shatter = serial.Serial('COM4', 115200, timeout=1)

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
    shatter.write((actual_cmd + '\n').encode('utf-8'))
    time.sleep(0.1)
    response = shatter.readline().decode('utf-8', errors='ignore').strip()
    print(f"送信: {normalized_label}（実信号: {actual_cmd}）")
    print(f"Arduino: {response}")

def main():
    # SHOT_304GS コントローラーで3軸制御のセッションを作成
    print("Initializing 3-axis stage controller...")
    stages = Session(Controllers.SHOT_304GS)

    # 3軸のステージを登録（X, Y, Z軸として使用）
    stages.append_stage(Stages.OSMS26_100)  # X軸
    stages.append_stage(Stages.OSMS26_100)  # Y軸
    stages.append_stage(Stages.OSMS26_100)  # Z軸
    # COM5に接続
    stages.connect(portname='COM5')
    stages.initialize()
    stages.set_speed(1, 1000, 10000, 500)
    stages.set_speed(2, 1000, 10000, 500)
    stages.set_speed(3, 1000, 10000, 500)

    # 現在位置を確認
    print("\nCurrent positions:")
    positions = stages.get_position()
    print(f"X-axis (stage 1): {positions[0]} µm")
    print(f"Y-axis (stage 2): {positions[1]} µm")
    print(f"Z-axis (stage 3): {positions[2]} µm")

    stages.move(amount=[39000, 65000, 80000], wait_for_finish=True)
    print("All axes movement complete")
    time.sleep(0.5)

    stages.move(amount=[0, -50000, -40000], wait_for_finish=True)

    time.sleep(0.5)

    stages.set_speed(3, 1000, 12000, 200)

    send_command("OPEN")
    time.sleep(0.5)

    stages.move(amount=[0, 0, -30000], wait_for_finish=True)

    send_command("CLOSE")
    time.sleep(0.5)


    stages.initialize()

    # 最終位置確認
    print("\nFinal positions:")
    positions = stages.get_position()
    print(f"X-axis (stage 1): {positions[0]} µm")
    print(f"Y-axis (stage 2): {positions[1]} µm")
    print(f"Z-axis (stage 3): {positions[2]} µm")

    print("\n=== Test completed ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
