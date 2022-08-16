### Dashboard template

- 다운로드
    
    `wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.2.0/aio/deploy/recommended.yaml`
    

### SA, CRB 설정

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

- token 생성
    
    `kubectl -n kubernetes-dashboard create token admin-user`
    
    - token 유효기간 설정
        
        → Deployment: spec : template: spec: conatainers: args:
        
        -  - -token-ttl = 86400(초) 추가
        

### Service(NodePort)

```yaml
kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 443
      targetPort: 8443
      nodePort: 30880
  type: NodePort
  selector:
    k8s-app: kubernetes-dashboard
```

```yaml
kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: dashboard-metrics-scraper
  name: dashboard-metrics-scraper
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 8000
      targetPort: 8000
      nodePort: 8000
  type: NodePort
  selector:
    k8s-app: dashboard-metrics-scraper
```

### 접근

`https://IP:30880/#/login`