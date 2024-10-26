package dev.deadline_destroyers.split_service.producers;

import dev.deadline_destroyers.split_service.dto.ResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class StompProducer {
    @Autowired
    private SimpMessagingTemplate template;
    public void send(ResponseDto responseDto) {
        var user = SecurityContextHolder.getContext()
                        .getAuthentication().getName();
        template.convertAndSendToUser(user, "/queue/messages" ,responseDto);
    }
}
