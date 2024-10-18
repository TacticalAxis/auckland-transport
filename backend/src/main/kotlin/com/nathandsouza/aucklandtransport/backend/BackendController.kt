package com.nathandsouza.aucklandtransport.backend

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/v1/auckland-transport/")
class BackendController {

    @GetMapping("get-data")
    fun getData(): String = "Here is some data"

}