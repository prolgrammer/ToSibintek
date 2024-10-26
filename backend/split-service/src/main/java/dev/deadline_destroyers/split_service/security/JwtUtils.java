package dev.deadline_destroyers.split_service.security;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import dev.deadline_destroyers.split_service.services.UuidService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.time.ZonedDateTime;

@Component
public class JwtUtils {
    @Value("${app.jwt.issuer}")
    private String issuer;

    @Value("${app.jwt.subject}")
    private String subject;

    @Value("${app.jwt.secret}")
    private String secret;

    @Value("${app.jwt.duration}")
    private Integer duration;

    @Autowired
    private UuidService uuidService;

    public String generate() {
        return JWT.create()
                .withIssuedAt(ZonedDateTime.now().toInstant())
                .withExpiresAt(ZonedDateTime.now().plusSeconds(duration).toInstant())
                .withClaim("id", uuidService.generate())
                .withSubject(subject)
                .withIssuer(issuer)
                .sign(Algorithm.HMAC256(secret));
    }

    public String verifyAndRetrieveId(String jwt) {
        var verifier = JWT.require(Algorithm.HMAC256(secret))
                .withClaimPresence("id")
                .withSubject(subject)
                .withIssuer(issuer)
                .build();
        var verifiedJwt = verifier.verify(jwt);
        return verifiedJwt.getClaim("id").asString();
    }



}
