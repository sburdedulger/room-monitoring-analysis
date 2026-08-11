#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11
#define MQ_PIN A0
#define RAIN_PIN A1

#define GAS_THRESHOLD 50
#define RAIN_THRESHOLD 150
#define SCREEN_DELAY 3000
#define BASELINE_ALPHA 0.02

LiquidCrystal_I2C lcd(0x27, 16, 2);
DHT dht(DHTPIN, DHTTYPE);

float gasBaseline = -1;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  dht.begin();

  lcd.setCursor(0, 0);
  lcd.print("Starting...");
  delay(1500);
  lcd.clear();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int gas = analogRead(MQ_PIN);
  int rain = analogRead(RAIN_PIN);

  if (gasBaseline < 0) {
    gasBaseline = gas;
  } else {
    if (abs(gas - gasBaseline) < 150) {
      gasBaseline = gasBaseline + BASELINE_ALPHA * (gas - gasBaseline);
    }
  }

  int gasDiff = gas - (int)gasBaseline;

  bool dhtOk = !(isnan(temperature) || isnan(humidity));

  // --- Screen 1: temperature & humidity ---
  lcd.clear();
  lcd.setCursor(0, 0);
  if (!dhtOk) {
    lcd.print("DHT11 error!");
  } else {
    lcd.print("Temp: ");
    lcd.print(temperature, 1);
    lcd.print((char)223);
    lcd.print("C");

    lcd.setCursor(0, 1);
    lcd.print("Humidity: ");
    lcd.print(humidity, 1);
    lcd.print(" %");
  }
  delay(SCREEN_DELAY);

// --- Screen 2: gas level ---
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Gas raw: ");
  lcd.print(gas);
  lcd.setCursor(0, 1);
  lcd.print("Diff: ");
  lcd.print(abs(gasDiff));
  lcd.print(abs(gasDiff) > GAS_THRESHOLD ? " HIGH!" : " Normal");
  delay(SCREEN_DELAY);

  // --- Screen 3: rain status ---
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Rain Sensor:");
  lcd.setCursor(0, 1);
  if (rain > RAIN_THRESHOLD) {
    lcd.print("RAINING!");
  } else {
    lcd.print("Dry (");
    lcd.print(rain);
    lcd.print(")");
  }
  delay(SCREEN_DELAY);

  // --- Serial log ---
  Serial.print("Temp: ");
  if (dhtOk) Serial.print(temperature); else Serial.print("NaN");
  Serial.print(" Humidity: ");
  if (dhtOk) Serial.print(humidity); else Serial.print("NaN");
  Serial.print(" Gas(raw): "); Serial.print(gas);
  Serial.print(" Baseline: "); Serial.print(gasBaseline);
  Serial.print(" Gas(diff): "); Serial.print(gasDiff);
  Serial.print(" Rain: "); Serial.println(rain);
}