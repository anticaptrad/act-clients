const std = @import("std");
pub const Client = struct { base_url: []const u8, pub fn init(base_url: []const u8) Client { return .{ .base_url = std.mem.trimRight(u8, base_url, "/") }; } pub fn url(self: Client, allocator: std.mem.Allocator, path: []const u8) ![]u8 { return std.fmt.allocPrint(allocator, "{s}{s}{s}", .{ self.base_url, if (std.mem.startsWith(u8, path, "/")) "" else "/", path }); } };
