# Init containers (Kubernetes)

Use an init container to bootstrap secrets into your pod before the main container starts — without installing the Kubernetes operator.

::: tip Prefer the operator
For production Kubernetes setups the [operator](/integrations/kubernetes) is easier to manage — it handles re-sync automatically and doesn't require changing every Deployment. Use init containers when you can't install cluster-wide CRDs.
:::

## How it works

1. The init container runs `snapenv pull` and writes the output to a shared `emptyDir` volume
2. The main container reads the file at startup
3. Secrets are in memory only — never in the image or persistent storage

## Pod manifest

```yaml
initContainers:
  - name: snapenv-init
    image: ghcr.io/snapenv-io/cli:latest
    command: ["snapenv", "pull", "--env", "prod", "--output", "/secrets/.env"]
    env:
      - name: SNAPENV_TOKEN
        valueFrom:
          secretKeyRef:
            name: snapenv-token
            key: token
      - name: SNAPENV_PROJECT
        value: "<your-project-uuid>"
    volumeMounts:
      - name: secrets
        mountPath: /secrets

containers:
  - name: app
    image: your-app:latest
    volumeMounts:
      - name: secrets
        mountPath: /secrets
        readOnly: true

volumes:
  - name: secrets
    emptyDir:
      medium: Memory   # tmpfs — never written to disk
```

## Create the token Secret

```bash
kubectl create secret generic snapenv-token \
  --from-literal=token=snp_live_xxxxxxxxxxxx
```

## Source the file in your app

```bash
# In your entrypoint or CMD
source /secrets/.env && exec node server.js
```

Or load it programmatically (Node.js example):

```js
import { config } from 'dotenv';
config({ path: '/secrets/.env' });
```
