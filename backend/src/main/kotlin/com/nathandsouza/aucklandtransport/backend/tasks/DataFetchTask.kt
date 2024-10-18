package com.nathandsouza.aucklandtransport.backend.tasks

import com.nathandsouza.aucklandtransport.backend.services.DataServiceInterface
import org.springframework.stereotype.Component

@Component
class DataFetchTask(private val dataService: DataServiceInterface) {

}