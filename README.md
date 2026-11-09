# ESP32 + MAX30102 PPG raw 데이터 수집 (Windows / macOS)

같은 **ESP32 펌웨어**와 **Python 수집 코드**를 Windows와 Mac에서 공통으로 사용합니다. Arduino IDE는 설치할 필요 없습니다.

## 1. 배선 (전원을 뺀 상태에서 연결)

| MAX30102 모듈 표기 | ESP32 핀 |
| --- | --- |
| VCC 또는 VIN | 3V3 |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |

센서 모듈의 실제 실크 인쇄를 확인하세요. **5V에 연결하지 마세요.** ESP32는 USB 데이터 케이블로 컴퓨터와 연결합니다.

## 2. ESP32 펌웨어 업로드 (Windows와 macOS 동일)

1. [VS Code](https://code.visualstudio.com/)를 설치합니다.
2. Extensions에서 **PlatformIO IDE**를 찾아 설치합니다. 별도 Arduino IDE는 불필요합니다.
3. VS Code에서 `File > Open Folder`로 이 폴더 전체를 엽니다.
4. USB로 ESP32를 연결합니다.
5. PlatformIO의 **Upload (→)** 버튼을 눌러 `src/main.cpp`를 보드에 업로드합니다.
6. 업로드가 끝나면 **Serial Monitor**에서 `sample,red,ir`와 숫자들이 나오는지 잠깐 확인할 수 있습니다.
7. **데이터 수집 전에는 Serial Monitor를 반드시 닫습니다**. 같은 USB 포트를 동시에 두 프로그램에서 사용할 수 없습니다.

`platformio.ini`는 일반적인 ESP32 Dev Module(`esp32dev`) 설정입니다. 다른 보드 변형이라면 보드 식별자를 확인해야 합니다.

## 3A. Windows에서 저장

1. [Python](https://www.python.org/downloads/windows/) 설치 (Python Launcher `py` 명령 사용 가능하도록 설치).
2. 이 폴더에서 명령 프롬프트(cmd)를 엽니다.
3. 연결된 포트 조회: `start_windows.bat list`.
4. 예를 들어 `COM5`가 보이면 30초 수집: `start_windows.bat COM5 30`.
5. `ppg_raw_날짜_시간.csv` 파일이 이 폴더에 저장됩니다.

시간 제한 없이 수집하려면 `start_windows.bat COM5` 명령을 실행하고 `Ctrl+C`로 중지합니다.

## 3B. macOS에서 저장

1. [Python](https://www.python.org/downloads/macos/) 설치 (`python3` 명령 사용 가능하도록 설치).
2. Terminal을 열고 이 폴더로 이동합니다. (예: `cd ~/Downloads/PPG_MAX30102_Windows_macOS`)
3. 연결된 포트 조회: `bash start_macos.sh list`.
4. 예를 들어 `/dev/cu.usbserial-110`이 보이면 30초 수집: `bash start_macos.sh /dev/cu.usbserial-110 30`.
5. `ppg_raw_날짜_시간.csv` 파일이 이 폴더에 저장됩니다.

시간 제한 없이 수집하려면 마지막 `30`을 빼고 실행한 뒤 `Ctrl+C`로 중지합니다.

**Mac에서는** `/dev/cu.usbserial-*`, `/dev/cu.wchusbserial*`, `/dev/cu.SLAB_USBtoUART` 등 기종별 포트 이름이 달라집니다. 항상 `list` 명령에 나온 실제 이름을 사용하세요.

## 4. CSV 예시

```csv
sample,red,ir
0,85432,76215
1,85521,76302
2,85689,76488
```

- `red`: 적색 LED에서 측정한 원시 ADC 값
- `ir`: 적외선 LED에서 측정한 원시 ADC 값
- `sample`: ESP32가 부팅된 뒤 기록한 샘플 번호
- 센서 설정: **100 samples/s**, FIFO 평균 1, Red+IR 두 채널
- BPM, SpO₂ 계산이나 소프트웨어 필터링은 하지 않습니다.

샘플 번호는 측정 주기 분석에 활용할 수 있지만, **하드웨어 절대 시간스탬프는 아닙니다**. USB 전송이나 수집 오류로 샘플이 누락될 수 있으니 긴 기록은 샘플 번호의 연속성을 확인하세요.

## 5. 문제 해결

- 포트 목록에 장치가 없음: USB가 충전 전용 케이블인지 확인하고, 보드에 사용된 USB-UART 칩에 맞는 드라이버(CP210x 또는 CH34x 등)가 필요한지 확인합니다.
- 업로드 실패: 다른 앱이 COM/`/dev/cu.*` 포트를 점유하지 않았는지 확인합니다. 일부 ESP32 보드는 업로드 중 `BOOT` 버튼이 필요할 수 있습니다.
- `MAX30102 not found`: 센서 3V3 전원, 공통 GND, GPIO21 SDA, GPIO22 SCL을 재확인합니다.
- CSV가 헤더만 있음: 업로드가 되었는지 확인하고 PlatformIO Serial Monitor에서 센서 연결 오류를 확인합니다.
- 15대 실습: 같은 펌웨어를 15대 각각 한 번씩 업로드하고, 학생마다 해당 컴퓨터의 포트를 선택하도록 안내하면 됩니다.

## 파일 구성

- `platformio.ini`: PlatformIO 설정
- `src/main.cpp`: ESP32 센서 펌웨어
- `record_ppg.py`: Windows/macOS 공용 CSV 수집 프로그램
- `start_windows.bat`: Windows용 설치·실행 도우미
- `start_macos.sh`: Mac용 설치·실행 도우미
