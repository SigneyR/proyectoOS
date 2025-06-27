#include <DHT.h>

#define DHTPIN 2     // Pin donde está conectado el DHT11
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();

  if (isnan(temperatura) || isnan(humedad)) {
    Serial.println("Error leyendo del DHT11");
  } else {
    // Crear JSON simple manualmente
    Serial.print("{\"temperatura\":");
    Serial.print(temperatura, 1);
    Serial.print(",\"humedad\":");
    Serial.print(humedad, 1);
    Serial.println("}");
  }
  delay(2000); // Espera 2 segundos entre lecturas
}
