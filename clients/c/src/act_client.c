#include "act_client.h"
act_client act_client_new(const char *base_url, const char *bearer_token) {
  act_client value = {base_url, bearer_token}; return value;
}
bool act_client_health(const act_client *client) { return client != 0 && client->base_url != 0; }
