#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>


static ESP8266WiFiMulti _Wifi;

static HTTPResponse Client_GET(String url)
{
    HTTPResponse response = { .code = 0, .payload = "" };

    if (_Wifi.run() == WL_CONNECTED)
    {
        WiFiClient client;
        HTTPClient https;
        if (https.begin(client, url))
        {
            response.code = https.GET();
            response.payload = https.getString();
            https.end();
        }
        else 
        {
            response.payload = "https GET failed.";
        }
    }
    else
    {
        response.payload = "wifi connection failed.";
    }

    Serial.println("Http GET response:");
    Serial.println(response.payload);
    return response;
}

HTTPResponse Client_POST(String url, String body)
{
    HTTPResponse response = { .code = 0, .payload = "" };

    if (_Wifi.run() == WL_CONNECTED)
    {
        WiFiClient client;
        HTTPClient https;
        if (https.begin(client, url))
        {
            https.addHeader("Content-Type", "application/json");
            response.code = https.POST(body);
            response.payload = https.getString();
            https.end();
        }
        else
        {
            response.payload = "https POST failed.";
        }
    }
    else
    {
        response.payload = "wifi connection failed.";
    }

    Serial.println("Http POST response:");
    Serial.println(response.payload);
    return response;
}

bool Client_Greeting(GreetingData* pData)
{
    String url;
    HTTPResponse response;
    StaticJsonDocument<256> json;
    DeserializationError err;
    
    // Send HTTP request.
        
    url = SERVER_URL + "/devices/greeting?name=" + DEVICE_NAME;
    response = Client_GET(url);
    if (response.code != 200)
    {
        return false;
    }

    // Process HTTP response.
        
    err = deserializeJson(json, response.payload);
    if (err)
    {
        return false;
    }

    if (NULL != pData)
    {
        pData->success = json["success"];
        pData->message = String(json["message"]);
    }
    return true;
}

bool Client_Register()
{    
    String url;
    String body;
    HTTPResponse response;
   
    // Send HTTP request.
     
    url = SERVER_URL + "/devices/register";
    body = "{\"name\":\"" + DEVICE_NAME + "\"}";
    
    response = Client_POST(url, body);
    if (response.code != 200)
    {
        return false;
    }
    return true;
}

void Client_Initialise( void )
{
    WiFi.mode(WIFI_STA);
    _Wifi.addAP(WIFI_NAME, WIFI_PASSWORD);

    Serial.printf("Http Client initialisation complete.\n");
}
