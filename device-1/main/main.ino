#include "globals.h"

void _Initialise()
{
    Serial.begin(115200);
    Serial.flush();
    delay(1000);
    
    Serial.printf("Hello World!\n");
    
    pinMode(LED_BUILTIN, OUTPUT);
    Server_Initialise();
    Client_Initialise();
}

void setup()
{
    _Initialise();
    
    Serial.printf("3 ...\n");
    delay(1000);
    Serial.printf("2 ...\n");
    delay(1000);
    Serial.printf("1 ...\n");
    delay(1000);

    Serial.printf("Run!\n");
}

void _Run()
{
    Server_Run();
    
    static unsigned long lastTime = 0;
    static GreetingData data;
    
    unsigned long now = millis();
    if ((now - lastTime) >= 5000)
    {
        lastTime = now;

        if (Client_Greeting(&data))
        {
            if (data.message.indexOf("meet") >= 0)
            {
                Client_Register();
            }
        }
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    }
}

void loop()
{
    _Run();
}
