const int MQ4_PIN = A0;
const int BUZZER_PIN = 8;
const int LED_PIN = 7;

const int WARMUP_TIME = 20000;  // MQ-4 needs ~20s to stabilize
const int SEND_INTERVAL = 500;  // ms between readings

unsigned long lastSendTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  Serial.println("Warming up MQ-4 sensor...");
  delay(WARMUP_TIME);
  Serial.println("Ready.");
}

void loop() {
  unsigned long now = millis();

  if (now - lastSendTime >= SEND_INTERVAL) {
    lastSendTime = now;
    int rawValue = analogRead(MQ4_PIN);
    Serial.println(rawValue);
  }
}