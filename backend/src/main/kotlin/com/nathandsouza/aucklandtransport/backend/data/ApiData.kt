package com.nathandsouza.aucklandtransport.backend.data

import org.springframework.data.annotation.Id
import org.springframework.data.mongodb.core.mapping.Document

@Document(collection = "data")
class ApiData {

    @Id
    val id: String? = null

    val data: String? = null

    val timestamp: Long = System.currentTimeMillis()
}