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

- you can build the cluster with terraform on gcloud: see this [k8s](https://github.com/giuliohome/gcp-k8s-sql-tf/tree/main/k8s) folder.
- you can use the [ingress](ingress.yaml) instead of kubectl port forwarding 
- notice also the header if you need to test by curl

```
giuliohome@cloudshell:~/flask-celery-microservice (my-cloud-giulio)$ curl -d "" -X POST  http://34.111.210.242/report
{"report_id":"10dd7a1f-a8a0-4b13-8a94-19cb582208dd"}
giuliohome@cloudshell:~/flask-celery-microservice (my-cloud-giulio)$ curl http://34.111.210.242/report/10dd7a1f-a8a0-4b13-8a94-19cb582208dd
{"id":"10dd7a1f-a8a0-4b13-8a94-19cb582208dd","result":null}
giuliohome@cloudshell:~/flask-celery-microservice (my-cloud-giulio)$ curl http://34.111.210.242/report/10dd7a1f-a8a0-4b13-8a94-19cb582208dd
{"id":"10dd7a1f-a8a0-4b13-8a94-19cb582208dd","result":{"state":"completed"}}
```

# celery worker running on Google Cloud

Just run a dockerized locust load testing
```
docker run -p 8089:8089 \
  -v $PWD:/mnt/locust \
  locustio/locust -f /mnt/locust/generate_flow_load_test.py
```

Simply use the cloud shell web preview on port 8089

![immagine](https://user-images.githubusercontent.com/3272563/156769262-f91b740e-f20c-4ad8-9cec-fb730d6c9d40.png)

# debugging postgres pod

First, you have to forward the pod port to the cloud shell
```
gcloud container clusters get-credentials my-cloud-giulio-dev-v1-mytf --region us-central1 --project my-cloud-giulio  && kubectl port-forward --namespace postgres $(kubectl get pod --namespace postgres --selector="name=postgresql" --output jsonpath='{.items[0].metadata.name}') 5432:5432
```
 run it in background or open another terminal and connect via psql

``` 
psql -h localhost -U test -d flask-service
```

then you can query the database
```
 flask-service=# SELECT * FROM celery_taskmeta where task_id='092b8d52-2118-44b8-b7dd-19410975648e';
 id |               task_id                | status  |                                  result                                  |         date_done          | traceback | name | args | kwargs | worker | retries | queue
----+--------------------------------------+---------+--------------------------------------------------------------------------+----------------------------+-----------+------+------+--------+--------+---------+-------
 15 | 092b8d52-2118-44b8-b7dd-19410975648e | SUCCESS | \x80059518000000000000007d948c057374617465948c09636f6d706c6574656494732e | 2022-03-04 11:18:45.167577 |           |      |      |        |        |         |
(1 row)
```

Another option is to [debug a pod](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-running-pod/), e.g

kubectl exec -it --namespace postgres postgresql-55566b698b-xdmzt -- sh

or to spin up an ephemeral debug container (with [net tools](https://github.com/nicolaka/netshoot))

## Announcement

![](https://github.com/kgrzybek/modular-monolith-with-ddd/raw/master/docs/Images/glory_to_ukraine.jpg)

Learn, use and benefit from this project only if:

- You **condemn Russia and its military aggression against Ukraine**
- You **recognize that Russia is an occupant that unlawfully invaded a sovereign state**
- You **support Ukraine's territorial integrity, including its claims over temporarily occupied territories of Crimea and Donbas**
- You **reject false narratives perpetuated by Russian state propaganda**

Otherwise, leave this project immediately and educate yourself.

Putin, idi nachuj.
