# 지능형신호처리 실습 · PPG 원시 데이터 수집

지능형신호처리 실습수업에서 사용할 **PPG 원시 데이터를 수집하고 CSV로 저장**하기 위한 저장소입니다. ESP32와 MAX30102로 적색(Red)·적외선(IR) 두 채널의 데이터를 수집합니다.

Windows와 macOS에서 같은 펌웨어와 Python 수집 프로그램을 사용합니다.

**수집 흐름:** 센서 연결 → 펌웨어 업로드 → CSV 저장

## 1. 준비물과 연결

- ESP32 개발 보드, MAX30102 센서 모듈, 점퍼선
- USB **데이터** 케이블
- [VS Code](https://code.visualstudio.com/)와 **PlatformIO IDE** 확장
- [Python 3](https://www.python.org/downloads/): Windows는 `py`, macOS는 `python3` 명령을 사용할 수 있도록 설치

**USB 전원을 분리한 상태에서** 다음과 같이 연결합니다.

| MAX30102 모듈 | ESP32 |
| --- | --- |
| VIN | 3V3 |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |

모듈의 핀 표기를 먼저 확인하세요. 이 실습에서는 **VIN을 3V3에 연결**합니다. 배선을 마친 뒤 ESP32를 USB 데이터 케이블로 컴퓨터에 연결합니다.

## 2. 펌웨어 업로드

1. VS Code의 `File > Open Folder`에서 이 저장소 폴더 전체를 엽니다.
2. ESP32를 USB로 연결합니다.
3. PlatformIO의 **Upload (→)**를 눌러 펌웨어를 업로드합니다.
4. **Serial Monitor**를 열어 `sample,red,ir` 형식의 숫자가 나오는지 확인합니다. 통신 속도는 **115200 baud**입니다.
5. 확인이 끝나면 **Serial Monitor를 종료**합니다. 모니터 터미널을 종료해 포트를 해제하세요.

> **CSV 수집 중에는 Serial Monitor를 켜두지 마세요.** 두 프로그램이 같은 시리얼 포트를 동시에 사용할 수 없습니다.

보드 설정은 [platformio.ini](platformio.ini)의 `esp32dev`입니다. 다른 ESP32 보드를 사용한다면 해당 보드에 맞게 설정을 확인합니다.

## 3. CSV로 데이터 저장

VS Code에서 `Terminal > New Terminal`을 열고, 현재 위치가 이 저장소 폴더인지 확인합니다. 첫 실행 시 실행 도우미가 `.venv`를 만들고 `pyserial`을 설치하므로 인터넷 연결이 필요합니다.

### Windows · PowerShell / cmd

연결된 포트를 확인합니다.

```powershell
.\start_windows.bat list
```

목록에서 ESP32에 해당하는 **USB 시리얼 포트**를 찾습니다. `CP210x`, `CH340` 등 USB-UART 장치 설명을 참고하고, Bluetooth 포트와 구분하세요.

아래는 **COM12가 ESP32 포트인 경우**의 예시입니다. 각자 조회한 포트 이름으로 바꿔 실행합니다.

```powershell
.\start_windows.bat COM12 30
```

### macOS · Terminal

연결된 포트를 확인합니다.

```bash
bash start_macos.sh list
```

목록에 나온 실제 포트 이름으로 실행합니다. 아래 이름은 예시입니다.

```bash
bash start_macos.sh /dev/cu.usbserial-110 30
```

포트 이름은 보드에 따라 `/dev/cu.usbserial-*`, `/dev/cu.wchusbserial*`, `/dev/cu.SLAB_USBtoUART` 등으로 표시될 수 있습니다.

### 측정과 저장 결과

1. 손가락을 센서의 측정면에 가볍게 올려 고정합니다.
2. 수집 명령을 실행하고, 측정 중 손가락과 센서가 움직이지 않도록 합니다.
3. 터미널의 `100 samples saved`와 같은 메시지로 저장 진행을 확인합니다.
4. 종료 후 이 저장소 폴더에 생성된 **`ppg_raw_날짜_시간.csv`**를 확인합니다.

마지막 인수 `30`은 초 단위의 수집 시간입니다. 시간 제한 없이 기록하려면 `30`을 생략하고, **`Ctrl+C`**로 종료합니다.

현재 프로그램은 포트 연결 후 2초간 기다린 다음 수집 시간을 잽니다. 이때 대기 중 버퍼에 쌓인 데이터도 저장될 수 있으므로, **30초 실행이 정확히 3,000개 샘플을 의미하지는 않습니다.**

## 4. 데이터 형식과 측정 설정

CSV의 첫 행은 열 이름이며, 이후 각 행에는 Red와 IR 한 쌍이 저장됩니다. 다음은 형식 예시입니다.

```csv
sample,red,ir
0,85432,76215
1,85521,76302
2,85689,76488
```

| 열 | 의미 |
| --- | --- |
| `sample` | ESP32가 읽어서 출력할 때 붙이는 순번. 보드가 재시작되면 0부터 시작 |
| `red` | 적색 LED로 측정한 원시 ADC 값 |
| `ir` | 적외선 LED로 측정한 원시 ADC 값 |

`red`와 `ir`는 ADC 카운트이며, 심박수나 산소포화도 값이 아닙니다.

| 설정 | 현재 값 |
| --- | --- |
| 채널 | Red + IR |
| 샘플링 주파수 | **100 Hz** · 채널당 초당 100개로 설정 |
| FIFO 평균화 | 1 · 평균화하지 않음 |
| LED 펄스 폭 / ADC 해상도 | 411 µs / 18 bit |
| ADC 범위 | 4096 nA |
| 시리얼 통신 | 115200 baud |

설정은 [src/main.cpp](src/main.cpp)의 `sensor.setup(0x1F, 1, 2, 100, 411, 4096)`에서 확인할 수 있습니다. 소프트웨어 필터링, 심박수 및 SpO₂ 계산은 수행하지 않습니다.

### 타임스탬프와 시간축

현재 CSV에는 개별 샘플의 측정 시각이 없습니다. **100 Hz로 누락 없이 수집됐다고 가정**하면, 첫 번째 저장 샘플을 기준으로 상대 시간을 계산할 수 있습니다.

```text
시간 [초] = (현재 sample - 첫 번째 저장 sample) / 100
```

위 가정에서 샘플 번호 차이가 1이면 0.01초, 100이면 1초에 해당합니다. 이는 설정된 샘플링 주파수를 기준으로 계산한 상대 시간입니다.

- 파일 이름의 날짜·시간은 PC에서 수집을 시작할 때 만든 값이며, 각 샘플의 측정 시각이 아닙니다.
- `sample`의 연속성으로 전송 도중 빠진 행이나 보드 재시작을 확인할 수 있습니다. 단, **센서 FIFO나 라이브러리 내부에서 발생한 누락까지 확인할 수는 없습니다.**
- PC가 데이터를 받은 시각은 센서의 측정 시각과 다릅니다. 다른 장비와의 정밀한 시간 동기화에는 추가적인 수집 설계가 필요합니다.

## 5. 문제 해결

| 증상 | 확인할 내용 |
| --- | --- |
| 포트 목록에 ESP32가 없음 | USB 데이터 케이블인지 확인하고, 보드의 USB-UART 칩에 맞는 드라이버 확인 |
| `Access denied` 또는 포트 열기 실패 | Serial Monitor와 같은 포트를 사용하는 프로그램을 종료하고, 포트 이름 재확인 |
| 업로드 실패 | 포트 점유 여부와 보드 설정 확인. 일부 보드는 업로드 연결 시 `BOOT` 버튼 조작 필요 |
| `MAX30102 not found` | 전원을 분리한 뒤 VIN–3V3, 공통 GND, SDA–GPIO21, SCL–GPIO22 배선 확인 |
| CSV에 `sample,red,ir`만 있음 | 실제 ESP32 포트인지 확인. 수집을 종료한 뒤 Serial Monitor에서 센서 오류 확인 |
| `py` / `python3` 명령을 찾을 수 없음 | Python 설치와 명령 실행 가능 여부를 확인한 뒤 터미널 다시 열기 |

## 6. 파일 구성

| 파일 | 역할 |
| --- | --- |
| [platformio.ini](platformio.ini) | 보드, 통신 속도, 센서 라이브러리 설정 |
| [src/main.cpp](src/main.cpp) | 센서 초기화, Red/IR 읽기, 시리얼 출력 |
| [record_ppg.py](record_ppg.py) | 시리얼 데이터 수신 및 CSV 저장 |
| [start_windows.bat](start_windows.bat) | Windows 실행 도우미 |
| [start_macos.sh](start_macos.sh) | macOS 실행 도우미 |

센서의 FIFO 구조와 설정에 대한 자세한 내용은 [MAX30102 데이터시트](https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf)를 참고하세요.
