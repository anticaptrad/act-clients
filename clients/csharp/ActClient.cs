namespace Anticaptrad;
public sealed class ActClient(string baseUrl) { private readonly string _baseUrl = baseUrl.TrimEnd('/'); public string Url(string path) => _baseUrl + (path.StartsWith('/') ? path : "/" + path); public string HealthUrl => Url("/health"); public string ReadyUrl => Url("/ready"); }
