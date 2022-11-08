# Health Check

强大的自愈能力是Kubernetes这类容器编排引擎的一个重要特性。自愈的默认实现方式是自动重启发生故障的容器。除此之外，用户还可以利用Liveness和Readiness探测机制设置更精细的健康检查，进而实现如下功能

- 零停机部署
- 避免部署无效的镜像
- 更加安全的滚动升级。

## 默认的健康检查

Kubernetes默认的健康检查机制：每个容器启动时都会执行一个进程，此进程由Dockerfile的CMD或ENTRYPOINT指定。如果进程退出时返回码非零，则认为容器发生故障，Kubernetes就会根据restartPolicy重启容器

下面模拟一个容器发生故障的场景，Pod的restartPolicy设置为OnFailure

```yaml
# healthcheck.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: pod
  name: healthcheck
spec:
  containers:
  - name: healthcheck
    args:
    - /bin/sh
    - -c
    - sleep 10; exit 1
    image: busybox
  restartPolicy: OnFailure
```

执行kubectl apply创建Pod，命名为healthcheck，过几分钟查看Pod的状态，可看到容器当前已经重启了2次

```shell
root@host3:~# kubectl apply -f healthcheck1.yaml
pod/healthcheck created
root@host3:~# kubectl get pods
NAME                            READY   STATUS    RESTARTS      AGE
healthcheck                     1/1     Running   2 (26s ago)   55s
```

在上面的例子中，容器进程返回值非零，Kubernetes则认为容器发生故障，需要重启。

## Liveness探测

有不少情况是发生了故障，但进程并不会退出。比如访问Web服务器时显示500内部错误，可能是系统超载，也可能是资源死锁，此时httpd进程并没有异常退出，在这种情况下重启容器可能是最直接、最有效的解决方案，需要通过Liveness探测来处理这类场景。

Liveness探测让用户可以自定义判断容器是否健康的条件。如果探测失败，Kubernetes就会重启容器。

### 例子

```yaml
# liveness.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: pod
  name: liveness
spec:
  restartPolicy: OnFailure
  containers:
  - name: liveness
    args:
    - /bin/sh
    - -c
    - touch /tmp/healthy; sleep 30;rm -rf /tmp/healthy; sleep 60
    image: busybox
    livenessProbe:
      exec:
        command:
        - cat
        - /tmp/healthy
      initialDelaySeconds: 10
      periodSeconds: 5
```

livenessProbe部分定义如何执行Liveness探测：

- 探测的方法是：通过cat命令检查/tmp/healthy文件是否存在。如果命令执行成功，返回值为零，Kubernetes则认为本次Liveness探测成功；如果命令返回值非零，本次Liveness探测失败
- initialDelaySeconds：10指定容器启动10之后开始执行Liveness探测，我们一般会根据应用启动的准备时间来设置。比如某个应用正常启动要花30秒，那么initialDelaySeconds的值就应该大于30
- periodSeconds：5指定每5秒执行一次Liveness探测。Kubernetes如果连续执行3次Liveness探测均失败，则会杀掉并重启容器

```shell
root@host3:~# kubectl apply -f liveness.yaml
pod/liveness created
```

通过kubectl describe pod liveness查看pod的日志，容器启动的前30s，/tmp/healthy存在，Liveness探测成功，events部分显示正常的日志

![image-20221108191649792](7-Health Check.assets/image-20221108191649792.png)

30s后，日志会显示/tmp/healthy已经不存在，Liveness探测失败，3次失败后容器就会重启

![image-20221108192026973](7-Health Check.assets/image-20221108192026973.png)

使用kubectl get pod liveness查看pod的重启次数

```shell
root@host3:~# kubectl get pod liveness
NAME       READY   STATUS    RESTARTS        AGE
liveness   1/1     Running   6 (2m28s ago)   10m
```

## Readiness探测

除了Liveness探测，Kubernetes Health Check机制还包括Readiness探测。

用户通过Liveness探测可以告诉Kubernetes什么时候通过重启容器实现自愈；Readiness探测则是告诉Kubernetes什么时候可以将容器加入到Service负载均衡池中，对外提供服务。

Readiness探测的配置语法与Liveness探测完全一样

```yaml
# readiness.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: pod
  name: readiness
spec:
  restartPolicy: OnFailure
  containers:
  - name: readiness
    args:
    - /bin/sh
    - -c
    - touch /tmp/healthy; sleep 30;rm -rf /tmp/healthy; sleep 60
    image: busybox
    readinessProbe:
      exec:
        command:
        - cat
        - /tmp/healthy
      initialDelaySeconds: 10
      periodSeconds: 5
```



Pod readiness的READY状态经历了如下变化：

- 刚被创建时，READY状态为不可用。
- 15秒后（initialDelaySeconds + periodSeconds），第一次进行Readiness探测并成功返回，设置READY为可用。
- 30秒后，/tmp/healthy被删除，连续3次Readiness探测均失败后，READY被设置为不可用。