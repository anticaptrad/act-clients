const std = @import("std");
pub fn build(b: *std.Build) void {
    const module = b.addModule("act_client", .{ .root_source_file = b.path("src/root.zig") });
    _ = module;
}
