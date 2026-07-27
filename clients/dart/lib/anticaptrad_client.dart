library;

import 'dart:convert';

import 'package:http/http.dart' as http;

final class ActHttpException implements Exception {
  const ActHttpException(this.status, this.body);

  final int status;
  final String body;

  @override
  String toString() => 'Act API returned HTTP $status';
}

final class ActClient {
  ActClient(String baseUrl, {http.Client? client})
    : baseUrl = baseUrl.replaceFirst(RegExp(r'/+$'), ''),
      _client = client ?? http.Client();

  final String baseUrl;
  final http.Client _client;

  Future<Map<String, Object?>> health() => _get('/health');

  Future<Map<String, Object?>> ready() => _get('/ready');

  Future<Map<String, Object?>> _get(String path) async {
    final request = http.Request('GET', Uri.parse('$baseUrl$path'))
      ..headers['accept'] = 'application/json'
      ..followRedirects = false;
    final streamed = await _client.send(request);
    final response = await http.Response.fromStream(streamed);
    if (response.statusCode < 200 || response.statusCode >= 300) {
      final body = response.body.length <= 1024
          ? response.body
          : response.body.substring(0, 1024);
      throw ActHttpException(response.statusCode, body);
    }
    return (jsonDecode(response.body) as Map).cast<String, Object?>();
  }

  void close() => _client.close();
}
