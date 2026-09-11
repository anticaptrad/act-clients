#ifndef ACT_CLIENT_H
#define ACT_CLIENT_H
#include <stddef.h>
typedef struct { const char *base_url; } act_client;
int act_client_url(const act_client *client, const char *path, char *out, size_t out_size);
#endif
