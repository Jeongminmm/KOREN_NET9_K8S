### Load Balancer란?

<aside>
💡 하나의 인터넷 서비스가 발생하는 트래픽이 많을 때 여러 대의 서버가 분산처리하여 서버의 로드율 증가, 부하량, 속도저하 등을 고려하여 적절히 분산처리하여 해결해주는 서비스

</aside>

- In K8S
    
    → 서비스를 외부에 노출시키는 표준 방법으로 LoadBalancer가 분산 Node들에 정의된 NodePort를 통해 로드밸런싱을 한 후 서비스가 Pod들 사이에서 로드밸런싱을 수행
    

### MetalLB란?

K8S Load Balancer는 클라우드 플랫폼(aws, azure 등) 기본적으로 제공(온프레미스 환경에서는 사용 불가) → metalLB **온프레미스 환경**(IDC)에서 사용할 수 있는 서비스 **:** L2 네트워크(ARP/NDP), L3 네트워크(BGP)로 Load Balancer를 구현

### 설치 환경

- Ubuntu 20.04
- Kubernetes v1.24.3
- Calico v3.23.3

### 사전 설정

- Kube-proxy IPVS mode 사용으로 인한 Strict ARP mode enable
    - Kubectl edit configmap -n kube-system kube-proxy
        
        → strictARP : false → true
        

### 설치

- namespace
    
    `kubectl apply -f [https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/namespace.yaml](https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/namespace.yaml)`
    
- metalLB
    
    `kubectl apply -f [https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/metallb.yaml](https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/metallb.yaml)`
    
- Secret
    
    `kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)" -o yaml --dry-run=client > metallb-secret.yaml`
    
    `kubectl apply -f metallb-secret.yaml`
    
- ConfigMap
    
    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      namespace: metallb-system
      name: config
    data:
      config: |
        address-pools:
        - name: default
          protocol: layer2
          addresses:  
          - 외부 IP
    ```
    

### 실습

- 예시 Service
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: nginx
    spec:
      selector:
        matchLabels:
          app: nginx
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: nginx:1
            ports:
            - name: http
              containerPort: 80
    ---
    
    apiVersion: v1
    kind: Service
    metadata:
      name: nginx
    spec:
      ports:
      - name: http
        port: 8001
        protocol: TCP
        targetPort: 80
      selector:
        app: nginx
      type: LoadBalancer
    ```