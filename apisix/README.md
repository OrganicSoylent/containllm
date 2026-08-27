# APISIX

APISIX is deployed via Helm using the values in `apisix_chart_values.yaml`.
The deployment uses **traditional mode** with etcd as the config provider and the ingress controller disabled.

## Files

| File | Purpose |
|------|---------|
| `apisix_chart_values.yaml` | Helm values for the APISIX release |
| `ollama-route.yaml` | Kubernetes Job that registers the Ollama upstream and catch-all route via the Admin API |

## Ollama route (`ollama-route.yaml`)

### What it does

The Job calls the APISIX Admin API (port 9180) after installation and creates:

1. **Upstream** `ollama-large-upstream` → `ollama-service-large.ollama.svc.cluster.local:11434`
2. **Route** `/*` (all HTTP methods) → that upstream, so every request entering APISIX is forwarded to `ollama-service-large`

The Job is annotated with `helm.sh/hook: post-install,post-upgrade`, meaning it re-runs on every `helm upgrade` as well.

### How to apply

**Option A – via Helm `extraDeploy` (recommended)**

Paste the Job spec from `ollama-route.yaml` into `apisix_chart_values.yaml` under the `extraDeploy` key so it is part of the same Helm release:

```yaml
extraDeploy:
  - apiVersion: batch/v1
    kind: Job
    metadata:
      name: apisix-ollama-route-setup
      ...
```

Helm will handle ordering and cleanup automatically on install and upgrade.

**Option B – apply separately after `helm install`**

```bash
kubectl apply -f apisix/ollama-route.yaml -n <apisix-namespace>
```

### Configuration to adjust

| Setting | Location | Default | Notes |
|---------|----------|---------|-------|
| `RELEASE` | shell script inside the Job | `apisix` | Must match your Helm release name |
| `NAMESPACE` | shell script inside the Job | `apisix` | Must match the namespace APISIX is deployed into |
| `API_KEY` | shell script inside the Job | `edd1c9f034335f136f87ad84b625c8f1` | Must match `apisix.admin.credentials.admin` in the values file |

The Admin API service URL is derived as:
```
http://<RELEASE>-apisix-admin.<NAMESPACE>.svc.cluster.local:9180
```
