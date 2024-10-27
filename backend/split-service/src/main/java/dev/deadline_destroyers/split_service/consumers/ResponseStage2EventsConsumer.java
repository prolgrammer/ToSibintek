package dev.deadline_destroyers.split_service.consumers;

import dev.deadline_destroyers.split_service.config.Topics;
import dev.deadline_destroyers.split_service.events.RequestStage2Event;
import dev.deadline_destroyers.split_service.events.RequestStage3Event;
import dev.deadline_destroyers.split_service.events.ResponseStage1Event;
import dev.deadline_destroyers.split_service.events.ResponseStage2Event;
import dev.deadline_destroyers.split_service.producers.RequestStage2EventsProducer;
import dev.deadline_destroyers.split_service.producers.RequestStage3EventsProducer;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class ResponseStage2EventsConsumer {
    @Autowired
    private RequestStage3EventsProducer producer;

    @RabbitListener(queues = Topics.RESPONSE_STAGE_2_EVENTS_TOPIC_QUEUE)
    public void handle(ResponseStage2Event event) {
        producer.send(RequestStage3Event.builder()
                .user(event.getUser())
                .service(event.getService())
                .request(event.getRequest())
                .build());
    }
}