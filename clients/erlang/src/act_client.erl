-module(act_client).
-export([new/1, health_path/0, ready_path/0]).
new(BaseUrl) -> #{base_url => BaseUrl}.
health_path() -> <<"/health">>.
ready_path() -> <<"/ready">>.
