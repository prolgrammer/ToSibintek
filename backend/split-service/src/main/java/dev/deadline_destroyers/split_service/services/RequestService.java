package dev.deadline_destroyers.split_service.services;

import dev.deadline_destroyers.split_service.dto.RequestDto;
import dev.deadline_destroyers.split_service.dto.ResponseDto;
import dev.deadline_destroyers.split_service.events.RequestStage1Event;
import dev.deadline_destroyers.split_service.producers.RequestStage1EventsProducer;
import dev.deadline_destroyers.split_service.producers.StompProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service
public class RequestService {
    @Autowired
    private RequestStage1EventsProducer producer;

    @Autowired
    private StompProducer stompProducer;

    public void createRequest(RequestDto requestDto) {
        var user = SecurityContextHolder.getContext()
                .getAuthentication().getName();
        var event = RequestStage1Event.builder()
                .user(user)
                .request(requestDto.getRequest());
    }
}
