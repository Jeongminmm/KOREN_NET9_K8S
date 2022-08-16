## 기초 설정

### root 계정 활성화(master, worker)

`sudo passwd root`

→ root 계정 비밀번호 설정

`su - root`

→ root 계정 로그인

`vi /etc/ssh/sshd_config`

`PermitRootLogin yes`

`PasswordAuthentication yes`

→ root 로그인 해제 및 비밀번호 인증 허용

`service sshd restart`

→ sshd 재시작

## 구축

### Docker 설치(master, worker)

`sudo apt-get update`

`sudo apt-get install ca-certificates`

`sudo apt-get install curl`

`sudo apt-get install gnupg`

`sudo apt-get install lsb-release`

`sudo apt-get upgrade`

`curl -fsSL https:*//download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg*`

→ Docker 공식 레파지토리에서 패키지를 다운 시 위변조 확인을 위한 GPG 키를 추가

```yaml
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

→ Stable repository 설정

`sudo apt-get update`

`sudo apt-get install docker-ce docker-ce-cli containerd.io`

`sudo docker version`

`sudo systemctl enable docker`

`sudo systemctl start docker`

### K8S 설치(master, worker)

`swapoff -a && sed -i '/swap/s/^/#/'  /etc/fstab`

→ kubelet 적절한 동작을 위해서 swap 사용 중지 설정

`sudo ufw disable`

→ 방화벽 해제

cd 

```yaml
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
```

`sudo sysctl --system`

→ iptable 설정 

sudo apt-get update

sudo apt-get install -y apt-transport-https ca-certificates curl

`sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https:*//packages.cloud.google.com/apt/doc/apt-key.gpg*`

→ 구글 클라우드 퍼블릭 키 다운로드

```yaml
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

→ 쿠버네티스 저장소 추가

`sudo apt-get update`

`sudo apt-get install -y kubelet kubeadm kubectl`

`sudo apt-mark hold kubelet kubeadm kubectl`

`sudo systemctl daemon-reload`

→ 쿠버네티스를 서비스 등록

`sudo systemctl restart kubelet`

→ 쿠버네티스 서비스 재시작

### 클러스터 구성(master)

`kubeadm init`

→ control-plane node 초기화 및 node 구성을 위한 토큰 발행

ex.  kubeadm join [ip]:6443  - -token ~~~~~~~ \ - -discovert-token-ca-cert-hash ~~~~~~~~

- error([ERROR CRI]: container runtime is not running: 발생 시
    
    `vi /etc/containerd/config.toml`
    
    → disabled_plugins 항목에서 CRI 제거
    
    `system restart containerd`
    

### **Pod 통신을 위한 CNI(Container Network Interface) 기반 Pod 네트워크 추가(master)**

`curl [https://docs.projectcalico.org/manifests/calico.yaml](https://docs.projectcalico.org/manifests/calico.yaml) -O`

`kubectl apply -f calico.yaml`

### Worker node join(worker)

`kubeadm join [ip]:6443  - -token ~~~~~~~ \ - -discovert-token-ca-cert-hash ~~~~~~~~`

```yaml
kubeadm join IP:6443 --token ~~~~~~~~~~~~~~~ --discovery-token-ca-cert-hash sha256:~~~~~~~~~~
```

→ master node에서 발행한 토큰

- error([ERROR CRI]: container runtime is not running: 발생 시
    
    `vi /etc/containerd/config.toml`
    
    → disabled_plugins 항목에서 CRI 제거
    
    `systemctl restart containerd`
    
- Node 추가
    
    `kubeadm token create`
    
    → token 생성
    
    `openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //’`
    
    → hash 생성
    

### 설치 확인

`kubectl get nodes -o wide`
