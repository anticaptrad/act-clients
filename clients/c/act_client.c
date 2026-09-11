#include "act_client.h"
#include <stdio.h>
#include <string.h>
int act_client_url(const act_client *client, const char *path, char *out, size_t out_size) { if (!client || !client->base_url || !path || !out || out_size == 0) return -1; size_t n = strlen(client->base_url); while (n && client->base_url[n-1] == '/') n--; int written = snprintf(out, out_size, "%.*s%s%s", (int)n, client->base_url, path[0] == '/' ? "" : "/", path); return written < 0 || (size_t)written >= out_size ? -1 : 0; }
