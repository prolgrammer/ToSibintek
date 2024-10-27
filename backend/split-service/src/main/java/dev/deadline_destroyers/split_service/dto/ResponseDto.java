package dev.deadline_destroyers.split_service.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ResponseDto {
    private String request;
    private String user;
    private String time;
    private String stage;
    private String service;
    private String solution;
}
