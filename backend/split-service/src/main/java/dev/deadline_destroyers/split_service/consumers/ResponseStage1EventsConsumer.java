package dev.deadline_destroyers.split_service.consumers;

import dev.deadline_destroyers.split_service.config.Topics;
import dev.deadline_destroyers.split_service.events.RequestStage2Event;
import dev.deadline_destroyers.split_service.events.ResponseStage1Event;
import dev.deadline_destroyers.split_service.producers.RequestStage2EventsProducer;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class ResponseStage1EventsConsumer {
    @Autowired
    private RequestStage2EventsProducer producer;

    @RabbitListener(queues = Topics.RESPONSE_STAGE_1_EVENTS_TOPIC_QUEUE)
    public void handle(ResponseStage1Event event) {
        producer.send(RequestStage2Event.builder()
                .user(event.getUser())
                .service(event.getService())
                .request(event.getRequest())
                .build());
    }
}
