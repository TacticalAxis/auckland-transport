plugins {
	java
	id("org.springframework.boot") version "3.5.0"
	id("io.spring.dependency-management") version "1.1.7"
	id("org.openapi.generator") version "7.13.0"
}

group = "com.nathandsouza.transporthq"
version = "0.0.1-SNAPSHOT"

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(21)
	}
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-data-jpa")
	implementation("org.springframework.boot:spring-boot-starter-data-mongodb")
	implementation("org.springframework.boot:spring-boot-starter-quartz")
	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation("io.swagger.core.v3:swagger-annotations:2.2.30")
	implementation("org.openapitools:jackson-databind-nullable:0.2.6")
	implementation("jakarta.validation:jakarta.validation-api:3.1.1")
	developmentOnly("org.springframework.boot:spring-boot-devtools")
	developmentOnly("org.springframework.boot:spring-boot-docker-compose")
	runtimeOnly("org.postgresql:postgresql")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testImplementation("org.springframework.boot:spring-boot-testcontainers")
	testImplementation("org.testcontainers:junit-jupiter")
	testImplementation("org.testcontainers:mongodb")
	testImplementation("org.testcontainers:postgresql")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

openApiGenerate {
	generatorName.set("spring")
	inputSpec.set("$rootDir/src/main/resources/openapi/gtfs-realtime-compat.yaml")
	outputDir.set("${layout.buildDirectory.get()}/generated/openapi")
	apiPackage.set("com.nathandsouza.transporthq.backend.api")
	apiNameSuffix.set("Users")
	modelPackage.set("com.nathandsouza.transporthq.backend.model")
	configOptions.set(mapOf(
		"interfaceOnly" to "true",
		"useSpringBoot3" to "true"
	))
}

sourceSets {
	main {
		java {
			srcDir("${layout.buildDirectory.get()}/generated/openapi/src/main/java")
		}
	}
}

tasks.named("compileJava") {
	dependsOn("openApiGenerate")
}


tasks.withType<Test> {
	useJUnitPlatform()
}
