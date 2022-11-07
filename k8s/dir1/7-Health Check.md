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

