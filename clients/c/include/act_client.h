#ifndef ACT_CLIENT_H
#define ACT_CLIENT_H
#include <stdbool.h>
typedef struct { const char *base_url; const char *bearer_token; } act_client;
act_client act_client_new(const char *base_url, const char *bearer_token);
bool act_client_health(const act_client *client);
#endif
