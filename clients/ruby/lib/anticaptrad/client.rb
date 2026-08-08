require 'net/http'; require 'json'; require 'uri'
module Anticaptrad
 class Client
  def initialize(base_url) @base_url=base_url.sub(%r{/+$}, '') end
  def get(path); uri=URI(@base_url+path); res=Net::HTTP.get_response(uri); raise "Act API returned HTTP #{res.code}" unless res.is_a?(Net::HTTPSuccess); JSON.parse(res.body) end
  def health = get('/health')
  def ready = get('/ready')
 end
end
