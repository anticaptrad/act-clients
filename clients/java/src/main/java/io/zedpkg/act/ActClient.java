package io.zedpkg.act;
import java.net.URI;
public record ActClient(URI baseUri, String bearerToken) {}
