#!/usr/bin/env python3
"""
3軸ステージ制御テストプログラム
X, Y, Z軸を順番に動かす簡単なテスト
"""

import sys
sys.path.append('./pyOptoSigma')

from pyOptoSigma import Session, Controllers, Stages
import time

def main():
    # SHOT_304GS コントローラーで3軸制御のセッションを作成
    print("Initializing 3-axis stage controller...")
    stages = Session(Controllers.SHOT_304GS)

    # 3軸のステージを登録（X, Y, Z軸として使用）
    stages.append_stage(Stages.OSMS26_100)  # X軸
    stages.append_stage(Stages.OSMS26_100)  # Y軸
    stages.append_stage(Stages.OSMS26_100)  # Z軸

    # COM5に接続
    print("Connecting to COM5...")
    stages.connect(portname='COM5')
    print("Connected successfully!")

    # 原点復帰（これにより位置が確定し、get_position()が安全に呼べる）
    print("\nInitializing stages (returning to origin)...")
    stages.initialize()
    print("Initialization complete!")

    # 現在位置を確認
    print("\nCurrent positions:")
    positions = stages.get_position()
    print(f"X-axis (stage 1): {positions[0]} µm")
    print(f"Y-axis (stage 2): {positions[1]} µm")
    print(f"Z-axis (stage 3): {positions[2]} µm")

    # テスト動作：各軸を順番に動かす
    print("\n=== Starting test movements ===\n")

    # X軸を+1mm移動
    print("Moving X-axis +1000 µm...")
    stages.move(stage=1, amount=1000, wait_for_finish=True)
    print("X-axis movement complete")
    time.sleep(0.5)

    # Y軸を+1mm移動
    print("Moving Y-axis +1000 µm...")
    stages.move(stage=2, amount=1000, wait_for_finish=True)
    print("Y-axis movement complete")
    time.sleep(0.5)

    # Z軸を+1mm移動
    print("Moving Z-axis +1000 µm...")
    stages.move(stage=3, amount=1000, wait_for_finish=True)
    print("Z-axis movement complete")
    time.sleep(0.5)

    # 現在位置を再確認
    print("\nPositions after movement:")
    positions = stages.get_position()
    print(f"X-axis (stage 1): {positions[0]} µm")
    print(f"Y-axis (stage 2): {positions[1]} µm")
    print(f"Z-axis (stage 3): {positions[2]} µm")

    # 元の位置に戻る（各軸を個別に戻す方が安全）
    print("\nReturning to original positions...")
    stages.move(stage=1, amount=-1000, wait_for_finish=True)
    stages.move(stage=2, amount=-1000, wait_for_finish=True)
    stages.move(stage=3, amount=-1000, wait_for_finish=True)

    # 移動完了を待つ
    while stages.is_busy():
        time.sleep(0.1)
    print("All axes returned to starting position")

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
