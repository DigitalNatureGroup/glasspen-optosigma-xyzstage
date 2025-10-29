#!/usr/bin/env python3
"""
3軸ステージ制御テストプログラム
X, Y, Z軸を順番に動かす簡単なテスト
"""

import time
import math
from pyOptoSigma.pyOptoSigma import Controllers, Session, Stages

def hexagonal_spiral(stages, radius=5000, z_per_turn=5000, num_turns=3):
    """
    6角形で近似した螺旋運動
    現在位置を右下の頂点として、そこから6角形を描く
    """

    print(f"Starting hexagonal spiral: {num_turns} turns")

    angles = [-60, 0, 60, 120, 180, 240]
    
    # 6つの頂点座標を計算（現在位置を-60度の位置とする）
    vertices = []
    for angle_deg in angles:
        angle_rad = math.radians(angle_deg)
        stage2 = radius * math.cos(angle_rad)
        stage1 = radius * math.sin(angle_rad)
        vertices.append((stage1, stage2))
    
    # 現在位置はすでに最初の頂点（-60度）にいるので移動不要
    
    # 螺旋を描く
    for turn in range(num_turns):
        for i in range(6):
            next_vertex = vertices[(i + 1) % 6]
            current_vertex = vertices[i]
            
            stage1 = next_vertex[0] - current_vertex[0]
            stage2 = next_vertex[1] - current_vertex[1]
            stage3 = -(z_per_turn / 6)
            
            print(f"Turn {turn+1}, Edge {i+1}: Moving [{stage1:.1f}, {stage2:.1f}, {stage3:.1f}]")
            
            stages.move(amount=[stage1, stage2, stage3], absolute=False, wait_for_finish=True)

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
    stages.set_speed(1, 500, 5000, 200) # 最低速度1～500000 最高速度1～500000 加減速時間0～1000
    stages.set_speed(2, 500, 5000, 200)
    stages.set_speed(3, 500, 5000, 200)

    # 現在位置を確認
    print("\nCurrent positions:")
    positions = stages.get_position()
    print(f"X-axis (stage 1): {positions[0]} µm")
    print(f"Y-axis (stage 2): {positions[1]} µm")
    print(f"Z-axis (stage 3): {positions[2]} µm")

    stages.move(amount=[39000, 65000, 80000], wait_for_finish=True)
    print("All axes movement complete")
    time.sleep(0.5)

        # 現在位置を再確認
    print("\nPositions after movement:")
    positions = stages.get_position()
    print(f"X-axis (stage 1): {positions[0]} µm")
    print(f"Y-axis (stage 2): {positions[1]} µm")
    print(f"Z-axis (stage 3): {positions[2]} µm")


    stages.set_speed(1, 4000, 5000, 200) # 最低速度1～500000 最高速度1～500000 加減速時間0～1000
    stages.set_speed(2, 4000, 5000, 200)
    stages.set_speed(3, 4000, 5000, 200)


    # # 円弧補間コマンドをそのまま送信 (半径 1 cm ≒ 5000 pulses)
    # # 90度の円弧: 終点 (+0, +0), 中心オフセット (+5000, 0)
    # arc_command = "E:W+P0+P0+P5000+P0"
    # print(f"Sending arc command: {arc_command}")
    # stages.move(amount=[0, 0, -30000], wait_for_finish=False)
    # stages._Session__send(arc_command)  # type: ignore[attr-defined]
    # stages._Session__send("G:")  # type: ignore[attr-defined]
    # stages._Session__wait_for_ready()  # type: ignore[attr-defined]
    # time.sleep(0.2)

    print("\n=== Starting hexagonal spiral motion ===")
    hexagonal_spiral(
        stages, 
        radius=500,      # 半径1mm
        z_per_turn=-10000, # 1周で10mm下降
        num_turns=3       # 3回転
    )


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
