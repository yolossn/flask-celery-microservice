# flask celery microservice

See the author's article [Scaling Celery workers with RabbitMQ on Kubernetes](https://learnk8s.io/scaling-celery-rabbitmq-kubernetes) for extended, interesting explanation: here below a few, relevant quotes from it.

# objective

> The Horizontal Pod Autoscaler (HPA) can be configured to increase and decrease the number of replicas based on metrics such as CPU and memory.

**What if you could use the number of messages in the queue to trigger the autoscaling instead?**

> Kubernetes does not understand custom metrics out of the box.

> However, you can use an event-driven autoscaler such as KEDA to collect and expose metrics to Kubernetes from databases (MySQL, Postgres), message queues (RabbitMQ, AWS SQS), telemetry systems (AWS Cloudwatch, Azure Monitor), etc.

> The data can be used in combination with the Horizontal Pod Autoscaler to create more Pods when the queue is full.

> Let's see this in action.

# alternative approaches (edge case)

> Since the Horizontal Pod Autoscaler (HPA) scales the replicas up and down based on the metrics, there is a chance that the HPA can kill a pod when it is processing a task.

*What if your task is really long and you don't want to stop it at all?*

> You should not use a Deployment (or ReplicaSet, or StatefulSet, etc.) but create individual Pods with an operator or use Kubernetes jobs.

# porting to Google Cloud

Done:

- you can use the ingress instead of kubectl port forwarding 
- notice also the header if you need to test by curl

```
giuliohome@cloudshell:~/flask-celery-microservice (my-cloud-giulio)$ curl -d "" -X POST  http://34.111.210.242/report
{"report_id":"10dd7a1f-a8a0-4b13-8a94-19cb582208dd"}
giuliohome@cloudshell:~/flask-celery-microservice (my-cloud-giulio)$ curl http://34.111.210.242/report/10dd7a1f-a8a0-4b13-8a94-19cb582208dd
{"id":"10dd7a1f-a8a0-4b13-8a94-19cb582208dd","result":null}
giuliohome@cloudshell:~/flask-celery-microservice (my-cloud-giulio)$ curl http://34.111.210.242/report/10dd7a1f-a8a0-4b13-8a94-19cb582208dd
{"id":"10dd7a1f-a8a0-4b13-8a94-19cb582208dd","result":{"state":"completed"}}
```