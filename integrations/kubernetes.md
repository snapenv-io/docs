# Kubernetes Operator

The SnapEnv operator automatically syncs variables into native Kubernetes Secrets. No init containers, no custom scripts — just a CRD and a controller.

## Install

```bash
kubectl apply -f https://get.snapenv.io/operator/install.yaml
```

Installs the CRD, RBAC, and operator Deployment into the `snapenv-operator` namespace.

## Quick start

**1. Create a token Secret:**

```bash
kubectl create secret generic snapenv-token \
  --from-literal=token=snp_live_xxxxxxxxxxxx
```

**2. Create a SnapEnvSecret resource:**

```yaml
apiVersion: snapenv.io/v1alpha1
kind: SnapEnvSecret
metadata:
  name: api-prod
  namespace: default
spec:
  tokenSecret: snapenv-token   # K8s Secret in same namespace
  project: <your-project-uuid>
  env: prod
  target: api-prod-env         # name of the K8s Secret to create
  syncInterval: 5m             # optional, default 5m
```

```bash
kubectl apply -f snapenvsecret.yaml
kubectl get ses api-prod   # watch the Ready column
```

**3. Mount in your Deployment:**

```yaml
envFrom:
  - secretRef:
      name: api-prod-env
```

## CRD reference

| Field | Required | Description |
|---|---|---|
| `tokenSecret` | yes | K8s Secret name containing the `snp_live_` token |
| `tokenKey` | no | Data key inside `tokenSecret` (default: `token`) |
| `project` | yes | SnapEnv project UUID |
| `env` | yes | SnapEnv environment name |
| `target` | yes | Name of the K8s Secret to create/update |
| `apiUrl` | no | Override API URL (default: `https://api.snapenv.io`) |
| `syncInterval` | no | Re-sync interval, min `1m` (default: `5m`) |

## Status fields

```bash
kubectl describe ses api-prod
```

| Field | Description |
|---|---|
| `ready` | `true` when last sync succeeded |
| `lastSyncTime` | Time of last successful sync |
| `lastSyncError` | Error message from last failed sync |
| `variableCount` | Number of variables written |

## Dashboard connection status

When the operator syncs, it sends `X-SnapEnv-Client: operator` with each pull request. The dashboard's **Integrations** page shows **Connected · last sync X ago** based on this.

## Troubleshooting

```bash
kubectl logs -n snapenv-operator deploy/snapenv-operator -f
kubectl get ses -A
kubectl describe ses <name>
```

| Error | Cause |
|---|---|
| `tokenSecret not found` | The named K8s Secret doesn't exist in the namespace |
| `HTTP 401` | Token is invalid or revoked |
| `HTTP 403` | Token lacks access to the project or environment |
| `HTTP 404` | Wrong project UUID or environment name |

## Update the operator

```bash
kubectl apply -f https://get.snapenv.io/operator/install.yaml
kubectl rollout restart deploy/snapenv-operator -n snapenv-operator
```
