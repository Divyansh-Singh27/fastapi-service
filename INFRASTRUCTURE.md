# Infrastructure Documentation — FastAPI on AWS ECS Fargate

> Complete AWS resource inventory for the **FastAPI service** deployed in the **techsimplus** account.

## Account & Region & **Pending Work**


| Property           | Value                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------- |
| **AWS Account ID** | `797671033939`                                                                          |
| **Region**         | `ap-south-1` (Mumbai)                                                                   |
| **Environment**    | `dev`                                                                                   |
| **Service**        | `techsimplus`                                                                           |
| **Provisioning**   | AWS CLI (manual, no Terraform)                                                          |
| **Repository**     | [Divyansh-Singh27/fastapi-service](https://github.com/Divyansh-Singh27/fastapi-service) |


### Common Tags Applied to All Resources


| Tag Key      | Value                                           |
| ------------ | ----------------------------------------------- |
| `Env`        | `dev`                                           |
| `Service`    | `techsimplus`                                   |
| `Components` | `<resource-type>` (e.g. `vpc`, `subnet`, `igw`) |
| `Name`       | `dev_techsimplus_`* (see each resource below)   |


> **Naming convention:** `{env}_{service}_{tier}_{mode}_{component}` — modeled on the reference architecture in the default account (`prod_studiomgmt_shared_o_`*). Here `m` denotes the mumbai  region.

---

## 1. Networking (VPC)

### VPC


| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Name**           | `dev_techsimplus_shared_m_vpc` |
| **VPC ID**         | `vpc-0e722105c6a459154`        |
| **CIDR Block**     | `10.0.0.0/16`                  |
| **DNS Hostnames**  | Enabled                        |
| **Components Tag** | `vpc`                          |


### Subnets


| Name                                      | Subnet ID                  | CIDR           | AZ            | Type          | Components |
| ----------------------------------------- | -------------------------- | -------------- | ------------- | ------------- | ---------- |
| `dev_techsimplus_shared_m_alb_public_1a`  | `subnet-0e85b359b00ac69de` | `10.0.1.0/24`  | `ap-south-1a` | Public (ALB)  | `subnet`   |
| `dev_techsimplus_shared_m_alb_public_1b`  | `subnet-01fee56c56be7e6a2` | `10.0.2.0/24`  | `ap-south-1b` | Public (ALB)  | `subnet`   |
| `dev_techsimplus_shared_m_app_private_1a` | `subnet-06254153fd00875b7` | `10.0.11.0/24` | `ap-south-1a` | Private (ECS) | `subnet`   |
| `dev_techsimplus_shared_m_app_private_1b` | `subnet-0813a697c860f1f28` | `10.0.12.0/24` | `ap-south-1b` | Private (ECS) | `subnet`   |


### Internet Gateway


| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Name**           | `dev_techsimplus_shared_m_igw` |
| **IGW ID**         | `igw-0efa7281bea419f9b`        |
| **Attached To**    | `vpc-0e722105c6a459154`        |
| **Components Tag** | `igw`                          |


### NAT Gateway


| Field              | Value                                                             |
| ------------------ | ----------------------------------------------------------------- |
| **Name**           | `dev_techsimplus_shared_m_nat_gateway_1`                          |
| **NAT Gateway ID** | `nat-07832b8b604446075`                                           |
| **Placed In**      | `dev_techsimplus_shared_m_alb_public_1a`                          |
| **Elastic IP**     | `dev_techsimplus_shared_m_nat_eip` (`eipalloc-017371f99f717ade2`) |
| **Components Tag** | `nat_gateway`                                                     |


### Route Tables


| Name                                             | Route Table ID          | Routes            | Associated Subnets   |
| ------------------------------------------------ | ----------------------- | ----------------- | -------------------- |
| `dev_techsimplus_shared_m_public_route_table`    | `rtb-07837316237c27782` | `0.0.0.0/0` → IGW | Both public subnets  |
| `dev_techsimplus_shared_m_private_route_table_1` | `rtb-0bf16c61c1bb33ab8` | `0.0.0.0/0` → NAT | Both private subnets |


### VPC Endpoints

> Required so Fargate tasks in private subnets can pull images from ECR and ship logs.


| Service                            | Endpoint ID              | Type      | State     |
| ---------------------------------- | ------------------------ | --------- | --------- |
| `com.amazonaws.ap-south-1.ecr.api` | `vpce-0641dfaf208363d1e` | Interface | available |
| `com.amazonaws.ap-south-1.ecr.dkr` | `vpce-0d1d0eb641c867e0c` | Interface | available |
| `com.amazonaws.ap-south-1.s3`      | `vpce-08d4434bb1c0b692d` | Gateway   | available |
| `com.amazonaws.ap-south-1.logs`    | `vpce-047954f019fbe2ef1` | Interface | available |


---

## 2. Security Groups

### ALB Security Group


| Field              | Value                         |
| ------------------ | ----------------------------- |
| **Name**           | `dev_techsimplus_external_sg` |
| **Group ID**       | `sg-0cb15b5064cf681c7`        |
| **Group Name**     | `fastapi-alb-sg`              |
| **Components Tag** | `sg`                          |


**Inbound Rules**


| Protocol | Port        | Source      |
| -------- | ----------- | ----------- |
| TCP      | 80 (HTTP)   | `0.0.0.0/0` |
| TCP      | 443 (HTTPS) | `0.0.0.0/0` |


### ECS Security Group


| Field              | Value                         |
| ------------------ | ----------------------------- |
| **Name**           | `dev_techsimplus_internal_sg` |
| **Group ID**       | `sg-06032147f62ace1ea`        |
| **Group Name**     | `fastapi-ecs-sg`              |
| **Components Tag** | `sg`                          |


**Inbound Rules**


| Protocol | Port | Source                          | Purpose              |
| -------- | ---- | ------------------------------- | -------------------- |
| TCP      | 8000 | `sg-0cb15b5064cf681c7` (ALB SG) | App traffic from ALB |
| TCP      | 443  | `10.0.0.0/16` (VPC CIDR)        | VPC endpoint access  |


---

## 3. Container Registry (ECR)


| Field                  | Value                                                           |
| ---------------------- | --------------------------------------------------------------- |
| **Name**               | `dev_techsimplus_fastapi_ecr`                                   |
| **Repository**         | `fastapi-service`                                               |
| **URI**                | `797671033939.dkr.ecr.ap-south-1.amazonaws.com/fastapi-service` |
| **Image Scan on Push** | Enabled                                                         |
| **Image Tags**         | `latest` + git commit SHA                                       |
| **Components Tag**     | `ecr`                                                           |


---

## 4. ECS (Fargate)

### Cluster


| Field                  | Value                                                                         |
| ---------------------- | ----------------------------------------------------------------------------- |
| **Name**               | `dev_techsimplus_fastapi_cluster`                                             |
| **ARN**                | `arn:aws:ecs:ap-south-1:797671033939:cluster/dev_techsimplus_fastapi_cluster` |
| **Capacity Providers** | `FARGATE`, `FARGATE_SPOT`                                                     |
| **Components Tag**     | `ecs_cluster`                                                                 |


### Task Definition


| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Family**         | `dev_techsimplus_fastapi_task` |
| **Launch Type**    | Fargate                        |
| **Network Mode**   | `awsvpc`                       |
| **CPU / Memory**   | 256 (.25 vCPU) / 512 MB        |
| **Architecture**   | `X86_64`                       |
| **Container Name** | `fastapi-service`              |
| **Container Port** | 8000                           |
| **Execution Role** | `ecsTaskExecutionRole`         |


### Service


| Field              | Value                             |
| ------------------ | --------------------------------- |
| **Name**           | `dev_techsimplus_fastapi_service` |
| **Cluster**        | `dev_techsimplus_fastapi_cluster` |
| **Desired Count**  | 1                                 |
| **Launch Type**    | Fargate                           |
| **Subnets**        | Both private app subnets          |
| **Security Group** | `sg-06032147f62ace1ea`            |
| **Public IP**      | Disabled                          |
| **Components Tag** | `ecs_service`                     |


### CloudWatch Log Group


| Field             | Value                          |
| ----------------- | ------------------------------ |
| **Name**          | `/ecs/dev-techsimplus-fastapi` |
| **Stream Prefix** | `ecs`                          |


---

## 5. Load Balancer (ALB)

### Application Load Balancer


| Field              | Value                                                                                                                |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| **Name**           | `dev-techsimplus-fastapi-alb`                                                                                        |
| **ARN**            | `arn:aws:elasticloadbalancing:ap-south-1:797671033939:loadbalancer/app/dev-techsimplus-fastapi-alb/5c274a26d744f3cf` |
| **DNS Name**       | `dev-techsimplus-fastapi-alb-93363427.ap-south-1.elb.amazonaws.com`                                                  |
| **Scheme**         | internet-facing                                                                                                      |
| **Subnets**        | Both public ALB subnets                                                                                              |
| **Security Group** | `sg-0cb15b5064cf681c7`                                                                                               |
| **Components Tag** | `alb`                                                                                                                |


### Target Group


| Field                     | Value                                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Name**                  | `dev-techsimplus-fastapi-tg`                                                                                   |
| **ARN**                   | `arn:aws:elasticloadbalancing:ap-south-1:797671033939:targetgroup/dev-techsimplus-fastapi-tg/418515ea137c40ed` |
| **Protocol / Port**       | HTTP / 8000                                                                                                    |
| **Target Type**           | `ip` (Fargate)                                                                                                 |
| **Health Check Path**     | `/health`                                                                                                      |
| **Health Check Interval** | 30s                                                                                                            |
| **Components Tag**        | `target_group`                                                                                                 |


### Listener


| Field               | Value                                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Protocol / Port** | HTTP / 80                                                                                                                         |
| **Default Action**  | Forward → `dev-techsimplus-fastapi-tg`                                                                                            |
| **ARN**             | `arn:aws:elasticloadbalancing:ap-south-1:797671033939:listener/app/dev-techsimplus-fastapi-alb/5c274a26d744f3cf/b4ee9d04842de2b3` |


---

## 6. Application Endpoints

Base URL: `http://dev-techsimplus-fastapi-alb-93363427.ap-south-1.elb.amazonaws.com`


| Method | Route           | Description                | Example Response                                             |
| ------ | --------------- | -------------------------- | ------------------------------------------------------------ |
| GET    | `/health`       | Health check (used by ALB) | `{"status":"healthy"}`                                       |
| GET    | `/about`        | Service metadata           | `{"service":"FastAPI ECS Service","version":"1.0.0",...}`    |
| GET    | `/greet?name=X` | Greeting                   | `{"message":"Hello, X! Welcome to FastAPI on ECS Fargate."}` |


---

## 7. CI/CD Pipeline (GitHub Actions)

**Workflow:** `.github/workflows/deploy.yml`
**Trigger:** push / merge to `main`

```
PR merge to main
      │
      ▼
Configure AWS credentials  (GitHub Secrets)
      │
      ▼
Login to ECR
      │
      ▼
Build Docker image  ──►  tag with git SHA + latest
      │
      ▼
Push to ECR
      │
      ▼
Render new task definition (inject image)
      │
      ▼
Deploy to ECS  ──►  wait-for-service-stability
```

### Required GitHub Secrets


| Secret                  | Purpose                   |
| ----------------------- | ------------------------- |
| `AWS_ACCESS_KEY_ID`     | IAM access key for deploy |
| `AWS_SECRET_ACCESS_KEY` | IAM secret key for deploy |


### Workflow Environment Variables


| Variable                 | Value                                           |
| ------------------------ | ----------------------------------------------- |
| `AWS_REGION`             | `ap-south-1`                                    |
| `ECR_REGISTRY`           | `797671033939.dkr.ecr.ap-south-1.amazonaws.com` |
| `ECR_REPOSITORY`         | `fastapi-service`                               |
| `ECS_CLUSTER`            | `dev_techsimplus_fastapi_cluster`               |
| `ECS_SERVICE`            | `dev_techsimplus_fastapi_service`               |
| `TASK_DEFINITION_FAMILY` | `dev_techsimplus_fastapi_task`                  |
| `CONTAINER_NAME`         | `fastapi-service`                               |


---

## 8. Architecture Diagram

```
                          Internet
                             │
                             ▼
              ┌──────────────────────────────┐
              │  ALB (internet-facing :80)   │  dev_techsimplus_external_sg
              │  public subnets 1a / 1b      │
              └──────────────┬───────────────┘
                             │ forward :8000
                             ▼
              ┌──────────────────────────────┐
              │  ECS Fargate Task            │  dev_techsimplus_internal_sg
              │  FastAPI :8000               │
              │  private subnets 1a / 1b     │
              └──────┬───────────────┬───────┘
                     │               │
            VPC Endpoints       NAT Gateway
          (ECR/S3/Logs)        (egress :443)
                     │               │
                     ▼               ▼
              ECR / CloudWatch    Internet (outbound)
```

---

## 9. Resource Quick Reference (IDs)

```
Account .............. 797671033939
Region ............... ap-south-1
VPC .................. vpc-0e722105c6a459154        (10.0.0.0/16)
Public Subnet 1a ..... subnet-0e85b359b00ac69de     (10.0.1.0/24)
Public Subnet 1b ..... subnet-01fee56c56be7e6a2     (10.0.2.0/24)
Private Subnet 1a .... subnet-06254153fd00875b7     (10.0.11.0/24)
Private Subnet 1b .... subnet-0813a697c860f1f28     (10.0.12.0/24)
IGW .................. igw-0efa7281bea419f9b
NAT Gateway .......... nat-07832b8b604446075
NAT EIP .............. eipalloc-017371f99f717ade2
Public RT ............ rtb-07837316237c27782
Private RT ........... rtb-0bf16c61c1bb33ab8
ALB SG ............... sg-0cb15b5064cf681c7
ECS SG ............... sg-06032147f62ace1ea
ECR .................. fastapi-service
ECS Cluster .......... dev_techsimplus_fastapi_cluster
ECS Service .......... dev_techsimplus_fastapi_service
Task Definition ...... dev_techsimplus_fastapi_task
ALB DNS .............. dev-techsimplus-fastapi-alb-93363427.ap-south-1.elb.amazonaws.com
VPCE ecr.api ......... vpce-0641dfaf208363d1e
VPCE ecr.dkr ......... vpce-0d1d0eb641c867e0c
VPCE s3 .............. vpce-08d4434bb1c0b692d
VPCE logs ............ vpce-047954f019fbe2ef1
Log Group ............ /ecs/dev-techsimplus-fastapi
```

---

## 10. Pending / Future Work

- [ ] **Route 53** DNS mapping to the ALB (alias record)
- [ ] **ACM certificate** + HTTPS (443) listener for TLS