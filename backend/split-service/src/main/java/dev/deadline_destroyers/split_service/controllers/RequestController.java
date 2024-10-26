package dev.deadline_destroyers.split_service.controllers;

import dev.deadline_destroyers.split_service.dto.RequestDto;
import dev.deadline_destroyers.split_service.services.RequestService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/requests")
public class RequestController {

    @Autowired
    private RequestService requestService;

    @PostMapping
    public ResponseEntity<Void> sendRequest(RequestDto requestDto) {
        requestService.createRequest(requestDto);
        return ResponseEntity.ok().build();
    }

}
