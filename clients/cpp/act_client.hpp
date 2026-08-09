#pragma once
#include <string>
#include <string_view>
namespace anticaptrad { class Client { std::string base_; public: explicit Client(std::string base): base_(std::move(base)) { while (!base_.empty() && base_.back()=='/') base_.pop_back(); } std::string url(std::string_view path) const { return base_ + (path.starts_with('/') ? "" : "/") + std::string(path); } std::string health_url() const { return url("/health"); } std::string ready_url() const { return url("/ready"); } }; }
