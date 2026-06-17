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
  syncInterval: 30m            # fallback poll interval (default 30m)
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

## Auto-restart deployments on change

Add the `snapenv.io/sync-secret` annotation to any Deployment or StatefulSet. When the operator detects that the variable content has changed (via content hash), it automatically triggers a rolling restart — no manual `kubectl rollout restart` needed.

The annotation value must match the `spec.target` name in your `SnapEnvSecret`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  annotations:
    snapenv.io/sync-secret: "api-prod-env"   # matches spec.target above
spec:
  template:
    spec:
      containers:
        - name: app
          envFrom:
            - secretRef:
                name: api-prod-env
```

The operator computes a SHA-256 hash of all variable values after every sync. If the hash matches the previous sync, no restart is triggered. Both `Deployment` and `StatefulSet` are supported.

## Smart polling — only syncs when something changed

The operator uses HTTP conditional requests so polls are nearly free when nothing has changed.

**How it works:**

1. On the first pull, the API returns the dotenv body plus an `ETag` header — a short hash of the variable content.
2. The operator stores that hash in `status.dataHash`.
3. On every subsequent poll, the operator sends `If-None-Match: "<hash>"` with the request.
4. If nothing changed, the API returns **`304 Not Modified`** with no body. The operator skips processing, skips the audit log, and re-schedules — the round trip costs almost nothing.
5. Only when variables actually change does the API return `200` with the new content, and only then does the operator update the Secret (and restart linked Deployments).

This means you can poll frequently without hammering the API or cluttering the audit log. The default `syncInterval` of `30m` is conservative — feel free to lower it:

```yaml
spec:
  syncInterval: 5m   # cheap — only does real work when variables change
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
| `syncInterval` | no | Fallback poll interval, min `1m` (default: `30m`) |

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
| `dataHash` | Content hash of the last synced variables — sent as `If-None-Match` on the next poll to get a cheap 304 when nothing changed |

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
