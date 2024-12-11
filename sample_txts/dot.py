import time
import os
import subprocess

# 파일 경로 설정
data_files = {
    3: ["life_3_1.txt", "life_3_2.txt"],
    2: ["life_2_1.txt", "life_2_2.txt"],
    1: ["life_1_1.txt", "life_1_2.txt"],
}

# 외부 CMD 창 열기
def open_cmd_window():
    if os.name == 'nt':  # Windows
        return subprocess.Popen("start cmd.exe /k python", shell=True)
    else:  # Unix-like 시스템
        return subprocess.Popen(["x-terminal-emulator", "-e", "python3"])

# 화면 지우기 함수
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# 도트 그래픽 출력 함수
def display_life(life):
    files = data_files.get(life, [])
    if not files:
        print("잘못된 생명 수!")
        return

    # FPS 효과 시뮬레이션 (빠른 전환)
    for _ in range(6):  # FPS처럼 빠르게 전환
        for file_path in files:
            clear_console()
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    print(file.read())
                time.sleep(0.5)  # 빠른 전환을 위한 짧은 대기 시간
            except Exception as e:
                print(f"파일 읽기 오류: {e}")

# 게임 실행 함수
def main():
    print("게임 시작! 🧠")
    time.sleep(2)

    for life in range(3, 0, -1):
        display_life(life)
        clear_console()  # 생명 감소 시 화면 초기화
        print(f"현재 생명: {life}개 남음!\n")
        time.sleep(1)

if __name__ == "__main__":
    main()
