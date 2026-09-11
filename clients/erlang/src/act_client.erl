-module(act_client).
-export([new/1, health_path/0, ready_path/0, new/2, base_url/1]).
new(BaseUrl) -> #{base_url => BaseUrl}.
health_path() -> <<"/health">>.
ready_path() -> <<"/ready">>.
new(BaseUrl, BearerToken) -> #{base_url => BaseUrl, bearer_token => BearerToken}.
base_url(Client) -> maps:get(base_url, Client).
