/* Ultra Pelican Bicycle 固件 — ESP32-C3 SuperMini
 * WiFi AP "PelicanBike" + 网页大按钮遥控（前进/后退/左转/右转/停）。
 * DRV8833 驱动 N20（方向+PWM 软启+限幅），MG90S 转向。
 * 安全：指令看门狗 800ms 无指令自动停车回中；PWM 限幅 80% 护电机。
 * 目标框架：Arduino-ESP32 core 3.x。引脚见 electronics/pinout.md。
 */
#include <WiFi.h>
#include <WebServer.h>

const char* AP_SSID = "PelicanBike";
const char* AP_PASS = "pelican123";

const int PIN_AIN1 = 4, PIN_AIN2 = 5, PIN_PWMA = 6;
const int PIN_SERVO = 7, PIN_LED = 10;

const int PWM_MAX = 204;          // 80% of 255，护 6V 电机于 7.4V
const unsigned long CMD_TIMEOUT = 800;

// LEDC API 版本隔离（Arduino-ESP32 core2 通道式 / core3 引脚式）
#if ESP_ARDUINO_VERSION_MAJOR >= 3
static void pwmAttach(int pin, uint32_t f, int res) { ledcAttach(pin, f, res); }
static void pwmWrite(int pin, uint32_t v) { ledcWrite(pin, v); }
#else
static void pwmAttach(int pin, uint32_t f, int res) { int ch = (pin == PIN_SERVO) ? 1 : 0; ledcSetup(ch, f, res); ledcAttachPin(pin, ch); }
static void pwmWrite(int pin, uint32_t v) { int ch = (pin == PIN_SERVO) ? 1 : 0; ledcWrite(ch, v); }
#endif

WebServer server(80);
int targetSpeed = 0;              // -255..255
int currentSpeed = 0;
int servoAngle = 90;
unsigned long lastCmd = 0;

const char PAGE[] PROGMEM = R"HTML(
<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pelican Bike</title><style>
body{font-family:system-ui;margin:0;display:flex;flex-direction:column;align-items:center;gap:14px;padding:24px;background:#111;color:#eee}
button{font-size:28px;padding:22px 34px;border-radius:16px;border:0;background:#2a6df4;color:#fff;min-width:120px}
button.stop{background:#d43a3a}
.row{display:flex;gap:14px}
</style></head><body>
<h2>鹈鹕自行车</h2>
<p style="color:#999">按住按钮运行，松开即停</p>
<div class="row"><button ontouchstart="down('f')" ontouchend="up()" onmousedown="down('f')" onmouseup="up()">前进</button></div>
<div class="row"><button ontouchstart="down('l')" ontouchend="up()" onmousedown="down('l')" onmouseup="up()">左转</button>
<button class="stop" ontouchstart="cmd('s')" onmousedown="cmd('s')">停</button>
<button ontouchstart="down('r')" ontouchend="up()" onmousedown="down('r')" onmouseup="up()">右转</button></div>
<div class="row"><button ontouchstart="down('b')" ontouchend="up()" onmousedown="down('b')" onmouseup="up()">后退</button></div>
<script>
function cmd(c){fetch('/cmd?c='+c).catch(()=>{});}
let hold=null;
function down(c){cmd(c); if(hold)clearInterval(hold); hold=setInterval(()=>cmd(c),300);}
function up(){if(hold){clearInterval(hold);hold=null;} cmd('s');}
</script></body></html>
)HTML";

void handleRoot() { server.send_P(200, "text/html", PAGE); }

void handleCmd() {
  String c = server.arg("c");
  lastCmd = millis();
  if (c == "f") targetSpeed = PWM_MAX;
  else if (c == "b") targetSpeed = -PWM_MAX;
  else if (c == "l") servoAngle = 60;
  else if (c == "r") servoAngle = 120;
  else { targetSpeed = 0; servoAngle = 90; }
  server.send(200, "text/plain", "ok");
}

void setMotor(int speed) {
  if (speed > 0) { digitalWrite(PIN_AIN1, HIGH); digitalWrite(PIN_AIN2, LOW); }
  else if (speed < 0) { digitalWrite(PIN_AIN1, LOW); digitalWrite(PIN_AIN2, HIGH); }
  else { digitalWrite(PIN_AIN1, LOW); digitalWrite(PIN_AIN2, LOW); }
  pwmWrite(PIN_PWMA, abs(speed));
}

void setServo(int angle) {
  // 50Hz(20ms) 16bit：0.5–2.5ms 脉宽映射 0–180°，换算占空比
  int us = map(angle, 0, 180, 500, 2500);
  pwmWrite(PIN_SERVO, (uint32_t)(us * 65535.0 / 20000.0));
}

void setup() {
  pinMode(PIN_AIN1, OUTPUT); pinMode(PIN_AIN2, OUTPUT);
  pinMode(PIN_PWMA, OUTPUT); pinMode(PIN_LED, OUTPUT);
  pwmAttach(PIN_PWMA, 20000, 8);
  pwmAttach(PIN_SERVO, 50, 16);
  setServo(90);
  WiFi.softAP(AP_SSID, AP_PASS);
  server.on("/", handleRoot);
  server.on("/cmd", handleCmd);
  server.begin();
  lastCmd = millis();
}

void loop() {
  server.handleClient();
  // 看门狗：无指令自动停车回中
  if (millis() - lastCmd > CMD_TIMEOUT) { targetSpeed = 0; servoAngle = 90; }
  // 软启/软停：每 10ms 逼近目标 8
  static unsigned long t = 0;
  if (millis() - t > 10) {
    t = millis();
    int d = targetSpeed - currentSpeed;
    currentSpeed += constrain(d, -8, 8);
    setMotor(currentSpeed);
    setServo(servoAngle);
    digitalWrite(PIN_LED, (millis() / 500) % 2);
  }
}