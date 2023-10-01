void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    
    Serial.begin(115200);
    Serial.flush();
    delay(1000);

    Serial.printf("Hello World!\n");
    Serial.flush();
    delay(1000);

    Serial.printf("3 ...\n");
    Serial.flush();
    delay(1000);

    Serial.printf("2 ...\n");
    Serial.flush();
    delay(1000);

    Serial.printf("1 ...\n");
    Serial.flush();
    delay(1000);

    Serial.printf("Run!\n");
    Serial.flush();
    delay(1000);
}

void loop()
{
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
}
