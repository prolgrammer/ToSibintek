package dev.deadline_destroyers.split_service.consumers;

import dev.deadline_destroyers.split_service.config.Topics;
import dev.deadline_destroyers.split_service.dto.ResponseDto;
import dev.deadline_destroyers.split_service.events.RequestStage3Event;
import dev.deadline_destroyers.split_service.events.RequestStage4Event;
import dev.deadline_destroyers.split_service.events.ResponseStage2Event;
import dev.deadline_destroyers.split_service.events.ResponseStage3Event;
import dev.deadline_destroyers.split_service.producers.RequestStage3EventsProducer;
import dev.deadline_destroyers.split_service.producers.RequestStage4EventsProducer;
import dev.deadline_destroyers.split_service.producers.StompProducer;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class ResponseStage3EventsConsumer {
    @Autowired
    private RequestStage4EventsProducer producer;

    @Autowired
    private StompProducer stompProducer;

    @RabbitListener(queues = Topics.RESPONSE_STAGE_3_EVENTS_TOPIC_QUEUE)
    public void handle(ResponseStage3Event event) {
        producer.send(RequestStage4Event.builder()
                .user(event.getUser())
                .service(event.getService())
                .request(event.getRequest())
                .response(event.getResponse())
                .build());
        stompProducer.send(ResponseDto.builder()
                        .stage("3")
                        .time(LocalDateTime.now().toString())
                        .solution(event.getResponse())
                        .service(event.getService())
                .build(), event.getUser());
    }
}