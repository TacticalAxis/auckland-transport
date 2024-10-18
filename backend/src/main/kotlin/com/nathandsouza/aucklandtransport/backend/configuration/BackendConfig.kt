package com.nathandsouza.aucklandtransport.backend.configuration

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.web.client.RestTemplate

@Configuration
class BackendConfig {

    @Bean
    fun restTemplate(): RestTemplate {
        return RestTemplate()
    }
}