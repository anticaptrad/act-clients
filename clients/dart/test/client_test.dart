import 'package:anticaptrad_client/anticaptrad_client.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:test/test.dart';

void main() {
  test('health uses the normalized base URL', () async {
    final transport = MockClient((request) async {
      expect(request.url.toString(), 'https://act.example/health');
      return http.Response('{"status":"ok"}', 200);
    });
    final client = ActClient('https://act.example/', client: transport);
    expect(await client.health(), {'status': 'ok'});
  });
}
