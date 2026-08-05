defmodule ActClient.MixProject do
  use Mix.Project
  def project, do: [app: :act_client, version: "0.1.0", elixir: "~> 1.15"]
  def application, do: [extra_applications: [:logger, :inets, :ssl]]
end
