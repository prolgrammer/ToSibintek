package dev.deadline_destroyers.split_service.consumers;

import dev.deadline_destroyers.split_service.config.Topics;
import dev.deadline_destroyers.split_service.events.RequestStage3Event;
import dev.deadline_destroyers.split_service.events.RequestStage4Event;
import dev.deadline_destroyers.split_service.events.ResponseStage2Event;
import dev.deadline_destroyers.split_service.events.ResponseStage3Event;
import dev.deadline_destroyers.split_service.producers.RequestStage3EventsProducer;
import dev.deadline_destroyers.split_service.producers.RequestStage4EventsProducer;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class ResponseStage3EventsConsumer {
    @Autowired
    private RequestStage4EventsProducer producer;

    @RabbitListener(queues = Topics.RESPONSE_STAGE_3_EVENTS_TOPIC_QUEUE)
    public void handle(ResponseStage3Event event) {
        producer.send(RequestStage4Event.builder()
                .user(event.getUser())
                .service(event.getService())
                .request(event.getRequest())
                .response(event.getResponse())
                .build());
    }
}