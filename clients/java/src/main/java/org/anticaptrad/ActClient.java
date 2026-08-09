package org.anticaptrad;
public final class ActClient { private final String baseUrl; public ActClient(String baseUrl){ this.baseUrl=baseUrl.replaceAll("/+$", ""); } public String url(String path){ return baseUrl + (path.startsWith("/") ? "" : "/") + path; } public String healthUrl(){ return url("/health"); } public String readyUrl(){ return url("/ready"); } }
