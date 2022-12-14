### Load Balancer๋?

<aside>
๐ก ํ๋์ ์ธํฐ๋ท ์๋น์ค๊ฐ ๋ฐ์ํ๋ ํธ๋ํฝ์ด ๋ง์ ๋ ์ฌ๋ฌ ๋์ ์๋ฒ๊ฐ ๋ถ์ฐ์ฒ๋ฆฌํ์ฌ ์๋ฒ์ ๋ก๋์จ ์ฆ๊ฐ, ๋ถํ๋, ์๋์ ํ ๋ฑ์ ๊ณ ๋ คํ์ฌ ์ ์ ํ ๋ถ์ฐ์ฒ๋ฆฌํ์ฌ ํด๊ฒฐํด์ฃผ๋ ์๋น์ค

</aside>

- In K8S
    
    โ ์๋น์ค๋ฅผ ์ธ๋ถ์ ๋ธ์ถ์ํค๋ ํ์ค ๋ฐฉ๋ฒ์ผ๋ก LoadBalancer๊ฐ ๋ถ์ฐ Node๋ค์ ์ ์๋ NodePort๋ฅผ ํตํด ๋ก๋๋ฐธ๋ฐ์ฑ์ ํ ํ ์๋น์ค๊ฐ Pod๋ค ์ฌ์ด์์ ๋ก๋๋ฐธ๋ฐ์ฑ์ ์ํ
    

### MetalLB๋?

K8S Load Balancer๋ ํด๋ผ์ฐ๋ ํ๋ซํผ(aws, azure ๋ฑ) ๊ธฐ๋ณธ์ ์ผ๋ก ์ ๊ณต(์จํ๋ ๋ฏธ์ค ํ๊ฒฝ์์๋ ์ฌ์ฉ ๋ถ๊ฐ) โ metalLB **์จํ๋ ๋ฏธ์ค ํ๊ฒฝ**(IDC)์์ ์ฌ์ฉํ  ์ ์๋ ์๋น์ค **:** L2 ๋คํธ์ํฌ(ARP/NDP), L3 ๋คํธ์ํฌ(BGP)๋ก Load Balancer๋ฅผ ๊ตฌํ

### ์ค์น ํ๊ฒฝ

- Ubuntu 20.04
- Kubernetes v1.24.3
- Calico v3.23.3

### ์ฌ์  ์ค์ 

- Kube-proxy IPVS mode ์ฌ์ฉ์ผ๋ก ์ธํ Strict ARP mode enable
    - Kubectl edit configmap -n kube-system kube-proxy
        
        โ strictARP : false โ true
        

### ์ค์น

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
          - ์ธ๋ถ IP
    ```
    

### ์ค์ต

- ์์ Service
    
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