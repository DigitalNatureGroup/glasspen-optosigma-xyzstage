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

    # 円弧の中心と半径 (PoC 用にハードコード)
    center_x_um = 85576.0
    center_y_um = 49966.0

    # Z は現在値を維持
    z_um = positions[2]

    print(f"\nMoving to arc start: X={center_x_um} µm, Y={center_y_um} µm")
    stages.move(amount=[center_x_um, center_y_um, z_um], absolute=True, wait_for_finish=True)
    time.sleep(0.2)

        # 現在位置を再確認
    print("\nPositions after movement:")
    positions = stages.get_position()
    print(f"X-axis (stage 1): {positions[0]} µm")
    print(f"Y-axis (stage 2): {positions[1]} µm")
    print(f"Z-axis (stage 3): {positions[2]} µm")

    # 円弧補間コマンドをそのまま送信 (半径 1 cm ≒ 5000 pulses)
    # 90度の円弧: 終点 (+0, +0), 中心オフセット (+5000, 0)
    arc_command = "E:W+P0+P0+P5000+P0"
    print(f"Sending arc command: {arc_command}")
    stages._Session__send(arc_command)  # type: ignore[attr-defined]
    stages._Session__send("G:")  # type: ignore[attr-defined]
    stages._Session__wait_for_ready()  # type: ignore[attr-defined]
    time.sleep(0.2)



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
