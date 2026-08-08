plugins {
    kotlin("jvm") version "2.0.21"
}

group = "org.anticaptrad"
version = "0.1.0"

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(17)
}
