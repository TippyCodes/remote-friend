#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>


static ESP8266WebServer server(80);

static void _HandleRoot()
{
    server.send(200, "text/plain", "hello from esp8266!\r\n");
}

static void _HandleNotFound()
{
    String message = "File Not Found\n\n";
    message += "URI: ";
    message += server.uri();
    message += "\nMethod: ";
    message += (server.method() == HTTP_GET) ? "GET" : "POST";
    message += "\nArguments: ";
    message += server.args();
    message += "\n";
    for (int i = 0; i < server.args(); i++)
    {
        message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
    }
    server.send(404, "text/plain", message);
}

void Server_Run()
{
    server.handleClient();
    MDNS.update();
}

void Server_Initialise()
{
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_NAME, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.println("Server waiting for WiFi ...");
    }
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    if (MDNS.begin("esp8266"))
    {
        Serial.println("MDNS responder started");
    }

    server.on("/", _HandleRoot);
    server.on("/inline", []() {
        server.send(200, "text/plain", "this works as well");
    });
    server.onNotFound(_HandleNotFound);

    server.begin();

    Serial.printf("Http Server initialisation complete.\n");
}
