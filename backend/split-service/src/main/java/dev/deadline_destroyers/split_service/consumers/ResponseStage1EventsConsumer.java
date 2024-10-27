package dev.deadline_destroyers.split_service.consumers;

import dev.deadline_destroyers.split_service.config.Topics;
import dev.deadline_destroyers.split_service.dto.ResponseDto;
import dev.deadline_destroyers.split_service.events.RequestStage2Event;
import dev.deadline_destroyers.split_service.events.ResponseStage1Event;
import dev.deadline_destroyers.split_service.producers.RequestStage2EventsProducer;
import dev.deadline_destroyers.split_service.producers.StompProducer;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class ResponseStage1EventsConsumer {
    @Autowired
    private RequestStage2EventsProducer producer;

    @Autowired
    private StompProducer stompProducer;

    @RabbitListener(queues = Topics.RESPONSE_STAGE_1_EVENTS_TOPIC_QUEUE)
    public void handle(ResponseStage1Event event) {
        producer.send(RequestStage2Event.builder()
                .user(event.getUser())
                .service(event.getService())
                .request(event.getRequest())
                .build());
        stompProducer.send(ResponseDto.builder()
                .stage("1")
                .time(LocalDateTime.now().toString())
                .service(event.getService())
                .build(), event.getUser());
    }
}
