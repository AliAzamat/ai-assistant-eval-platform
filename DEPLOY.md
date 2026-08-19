# Deploying the platform on AWS

The Compose stack maps cleanly onto managed AWS services.

## Build & push
    docker build -t $ECR/saep-platform:$GIT_SHA .
    aws ecr get-login-password | docker login --username AWS --password-stdin $ECR
    docker push $ECR/saep-platform:$GIT_SHA

## Managed services (replace the compose containers)
- **api** → ECS Fargate service behind an Application Load Balancer.
  The ALB must allow long-lived connections for the `/metrics/stream` SSE route.
- **postgres** → Amazon RDS for PostgreSQL (multi-AZ in prod).
- **redis** → Amazon ElastiCache for Redis (traces + pub/sub + agent state + quality).

## Secrets
`OPENAI_API_KEY` and `DATABASE_URL` come from AWS SSM Parameter Store / Secrets
Manager — never baked into the image.

## Promotion is eval-gated
CI calls `promote(...)`; if `regressed()` is True the build fails and the old
prompt version stays active. A worse assistant can never reach production.
