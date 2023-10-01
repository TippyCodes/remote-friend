static const String DEVICE_NAME = "Friend_1";

static const char* WIFI_NAME = "Alpaca";
static const char* WIFI_PASSWORD = "CatCatCat";

static const String SERVER_URL = "http://192.168.214.243:8000";

typedef struct
{
    int code;
    String payload;

} HTTPResponse;

typedef struct
{
    bool success;
    String message;

} GreetingData;
