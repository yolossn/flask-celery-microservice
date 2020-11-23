# flask-celery-microservice


# Install
### rabbitmq 

> helm install rabbitmq -f rabbitmq_values.yaml bitnami/rabbitmq

```yaml
plugins: "rabbitmq_management"

auth:
  username: admin
  password: secretpassword

volumePermissions:
  enabled: true
```

### postgres

> helm install postgres -f postgres_values.yaml bitnami/postgresql

```yaml
global:
  postgresql:
    postgresqlDatabase: flask-service
    postgresqlUsername: test
    postgresqlPassword: test@123

volumePermissions:
  enabled: true
```
