import time
import os

# 파일 경로 설정
data_files = {
    3: ["life_3_1.txt", "life_3_2.txt"],
    2: ["life_2_1.txt", "life_2_2.txt"],
    1: ["life_1_1.txt", "life_1_2.txt"],
}

# 화면 지우기 함수
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# 도트 그래픽 출력 함수
def display_life(life):
    files = data_files.get(life, [])
    if not files:
        print("잘못된 생명 수!")
        return

    for _ in range(3):
        for file_path in files:
            clear_console()
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    print(file.read())
                time.sleep(1)
            except Exception as e:
                print(f"파일 읽기 오류: {e}")

# 게임 실행 함수
def main():
    print("게임 시작! 🧠")
    time.sleep(2)

    for life in range(3, 0, -1):
        display_life(life)
        print(f"현재 생명: {life}개 남음!\n")
        time.sleep(1)

if __name__ == "__main__":
    main()
