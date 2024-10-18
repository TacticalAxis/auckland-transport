package com.nathandsouza.aucklandtransport.backend.services

import org.springframework.stereotype.Service
import org.springframework.web.client.RestTemplate
import org.springframework.web.client.getForObject

@Service
class DataServiceImpl(private val restTemplate: RestTemplate) : DataServiceInterface {

    override fun fetchDataFromApi() : String {
//        TODO("Not yet implemented")
        var apiUrl = "https://httpbin.org/get";
        return restTemplate.getForObject<String>(apiUrl);
    }
}