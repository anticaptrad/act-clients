// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "ActClient",
    platforms: [.iOS(.v15), .macOS(.v12)],
    products: [.library(name: "ActClient", targets: ["ActClient"])],
    targets: [.target(name: "ActClient")]
)
