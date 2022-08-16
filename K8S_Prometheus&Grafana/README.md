### Prometheus란?

→ 프로메테우스는 현재 가장 많이 사용되고 있는 쿠버네티스 모니터링 시스템

### Grafana란?

→그라파나는 지표를 분석, 시각화하는 오픈소스 도구로 주로 인프라 정보 및 분석 데이터 시각화를 위한 대시보드

### 설치 과정

- `kubectl create namespace monitoring`
    
    → namespace 생성
    
- `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
    
    → helm chart 등록
    
- `helm repo update`
    
    → 등록된 repo update
    
- `helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring`
    
    → helm을 통한 prometheus&grafana 설치
    
- prometheus-grafana deployment 수정
    
    → nodeSelector 추가
    
- prometheus-grafana service 변경(ClusterIP → NodePort)

### 접속

[](http://IP:30000/)

- ID/Password
    - admin
    - admin

- 모니터링 설정
    [Dashboards](https://grafana.com/grafana/dashboards/?search=kubernetes)