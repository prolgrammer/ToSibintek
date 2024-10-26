package dev.deadline_destroyers.split_service.services;

import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class UuidService {
    public String generate() {
        return UUID.randomUUID().toString();
    }
}
