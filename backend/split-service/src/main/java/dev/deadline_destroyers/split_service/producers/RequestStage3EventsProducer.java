package dev.deadline_destroyers.split_service.producers;


import dev.deadline_destroyers.split_service.config.Topics;
import dev.deadline_destroyers.split_service.events.RequestStage1Event;
import dev.deadline_destroyers.split_service.events.RequestStage3Event;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class RequestStage3EventsProducer {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(RequestStage3Event event) {
        rabbitTemplate.convertAndSend(Topics.REQUEST_STAGE_1_EVENTS_TOPIC, event.getUser(), event);
    }
}
