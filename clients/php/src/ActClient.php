<?php
namespace Anticaptrad;
final class ActClient { public function __construct(private string $baseUrl) { $this->baseUrl=rtrim($baseUrl,'/'); } public function url(string $path): string { return $this->baseUrl.'/'.ltrim($path,'/'); } public function healthUrl(): string { return $this->url('/health'); } public function readyUrl(): string { return $this->url('/ready'); } }
