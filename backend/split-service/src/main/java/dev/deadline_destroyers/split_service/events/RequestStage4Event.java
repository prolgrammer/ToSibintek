package dev.deadline_destroyers.split_service.events;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RequestStage4Event {
    private String user;
    private String docs;
    private String request;
    private String service;
}
