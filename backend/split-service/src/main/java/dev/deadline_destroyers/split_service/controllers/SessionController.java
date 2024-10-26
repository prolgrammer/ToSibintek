package dev.deadline_destroyers.split_service.controllers;

import dev.deadline_destroyers.split_service.security.JwtUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/generate-session")
public class SessionController {
    @Autowired
    private JwtUtils jwtUtils;

    @GetMapping
    public ResponseEntity<String> get() {
        return ResponseEntity.ok(jwtUtils.generate());
    }
}
