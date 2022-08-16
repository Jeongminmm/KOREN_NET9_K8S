### Stateful이란?

 app이 각각의 역할을 함(자신의 고유 역할을 가짐)

- app이 죽으면 같은 기능을 하는 app을 재생성(이름이 같아야 함 → 식별 요소이기 때문)
- 각각 다른 Volume을 가져야 함
- 기능에 맞게 트래픽 분산 → 목적에 따라 해당 Pod에 연결하기 위해 **Headless Service**
- ex. DB

→ **StatefulSet**

### NFS란?

**네트워크에 파일을 저장하는 메커니즘**으로 사용자가 원격 컴퓨터에 있는 파일 및 디렉토리에 액세스할 수 있고 해당 파일 및 디렉토리가 로컬에 있는 것처럼 처리하도록 허용하는 분산 파일 시스템

### 사전 설정 - Volume Mount

- Volume Mount
    
    `sudo mkfs –t ext4 /dev/vdb`
    
- 생성된 볼륨과 mount할 dir 생성
    
    `mkdir /mysqldb`
    
- mount
    
    `sudo mount /dev/vdb/ /mysqldb`
    
- 확인
    
    `df -f .`
    

### NFS 설치

- Mount할 폴더 이동
- 권한 설정
    
    `chmod -R 755 /mysqldb`
    
- 소유자 변경
    
    `chown -R 999:999 /mysqldb`
    
- NFS install
    
    `apt-get install nfs-common nfs-kernel-server rpcbind`
    
- read,write 권한 부여
    
    `vi etc/exports`
    
    → /mysqldb *(rw,sync,no_root_squash) 추가
    

### PV, PVC

- PV
    
    ```yaml
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: nfs-pv
    spec:
      capacity:
        storage: 20Gi
      volumeMode: Filesystem
      accessModes:
      - ReadWriteMany
      nfs:
        path: "/mysqldb/mysql"
        server: "서버IP"
    ```
    
- PVC
    
    ```yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: my-nfs-pvc
    spec:
      accessModes:
      - ReadWriteMany
      resources:
        requests:
          storage: 20Gi
    
    ```
    

### StatefulSet

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: database
data:
  MYSQL_ROOT_PASSWORD: 'mysql_password'
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - image: mysql:8.0.26
        name: mysql
        envFrom: 
        - configMapRef:
            name: database
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: my-nfs-pvc
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  type: NodePort
  ports:
    - port: 3306
      targetPort: 3306
      nodePort: 30306
  selector: 
    app: mysql

---
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  ports:
    - port: 30306
      targetPort: 3306
  selector:
    app: mysql
  type: LoadBalancer
```