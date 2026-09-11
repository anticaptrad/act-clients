package org.anticaptrad
class ActClient(baseUrl: String) { private val base = baseUrl.trimEnd('/'); fun url(path: String) = base + if (path.startsWith('/')) path else "/$path"; fun healthUrl() = url("/health"); fun readyUrl() = url("/ready") }
