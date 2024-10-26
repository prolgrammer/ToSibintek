package dev.deadline_destroyers.split_service.config;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitConfig {
    @Bean
    public TopicExchange queryStage1EventsTopic() {
        return new TopicExchange(Topics.REQUEST_STAGE_1_EVENTS_TOPIC);
    }

    @Bean
    public Queue queryStage1EventsTopicQueue() {
        return new Queue(Topics.REQUEST_STAGE_1_EVENTS_TOPIC_QUEUE);
    }

    @Bean
    public Binding stage1binding () {
        return BindingBuilder.bind(queryStage1EventsTopicQueue())
                .to(queryStage1EventsTopic()).with(Topics.REQUEST_STAGE_1_EVENTS_TOPIC);
    }

    @Bean
    public TopicExchange queryStage2EventsTopic() {
        return new TopicExchange(Topics.REQUEST_STAGE_2_EVENTS_TOPIC);
    }

    @Bean
    public Queue queryStage2EventsTopicQueue() {
        return new Queue(Topics.REQUEST_STAGE_2_EVENTS_TOPIC_QUEUE);
    }

    @Bean
    public Binding stage2binding () {
        return BindingBuilder.bind(queryStage2EventsTopicQueue())
                .to(queryStage2EventsTopic()).with(Topics.REQUEST_STAGE_2_EVENTS_TOPIC);
    }

    @Bean
    public TopicExchange queryStage3EventsTopic() {
        return new TopicExchange(Topics.REQUEST_STAGE_3_EVENTS_TOPIC);
    }

    @Bean
    public Queue queryStage3EventsTopicQueue() {
        return new Queue(Topics.REQUEST_STAGE_3_EVENTS_TOPIC_QUEUE);
    }

    @Bean
    public Binding stage3binding () {
        return BindingBuilder.bind(queryStage3EventsTopicQueue())
                .to(queryStage3EventsTopic()).with(Topics.REQUEST_STAGE_3_EVENTS_TOPIC);
    }

    @Bean
    public TopicExchange queryStage4EventsTopic() {
        return new TopicExchange(Topics.REQUEST_STAGE_4_EVENTS_TOPIC);
    }

    @Bean
    public Queue queryStage4EventsTopicQueue() {
        return new Queue(Topics.REQUEST_STAGE_4_EVENTS_TOPIC_QUEUE);
    }

    @Bean
    public Binding stage4binding () {
        return BindingBuilder.bind(queryStage4EventsTopicQueue())
                .to(queryStage4EventsTopic()).with(Topics.REQUEST_STAGE_4_EVENTS_TOPIC);
    }


}
