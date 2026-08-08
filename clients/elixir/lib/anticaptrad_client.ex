defmodule AnticaptradClient do
 defstruct [:base_url]
 def new(base_url), do: %__MODULE__{base_url: String.trim_trailing(base_url, "/")}
 def health_path, do: "/health"
 def ready_path, do: "/ready"
end
