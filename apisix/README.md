# APISIX

APISIX is deployed via Helm using the values in `apisix_chart_values.yaml`.
The deployment uses **standalone mode** — routes and upstreams are defined directly in the values file as YAML and stored in a ConfigMap. APISIX hot-reloads the ConfigMap automatically. No etcd, no Admin API calls, no Jobs required.

## Files

| File | Purpose |
|------|---------|
| `apisix_chart_values.yaml` | Helm values for the APISIX release — routes are defined here |
| `ollama-route.yaml` | Standalone reference copy of the route definition (not applied directly) |

## How routing works (standalone mode)

All route configuration lives under `apisix.deployment.standalone.config` in `apisix_chart_values.yaml`. The Helm chart turns this into a ConfigMap that APISIX mounts and watches.

To add or change a route:
1. Edit `apisix_chart_values.yaml` under `apisix.deployment.standalone.config`
2. Run `helm upgrade`

```bash
helm upgrade apisix apisix/apisix -f apisix/apisix_chart_values.yaml -n <namespace>
```

APISIX picks up the updated ConfigMap within seconds — no pod restart needed.

## Ollama route

The current route forwards **all traffic** entering APISIX to `ollama-service-large`:

```yaml
routes:
  - id: ollama-route
    uri: /*
    methods: [GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS]
    upstream:
      type: roundrobin
      nodes:
        "ollama-service-large.ollama.svc.cluster.local:11434": 1
      scheme: http
      pass_host: pass
#END
```

> The `#END` marker at the bottom is required — APISIX uses it to detect that the config file is complete.

## Adding more routes

Append additional route entries under `routes:` in the standalone config block, then run `helm upgrade`. Example:

```yaml
routes:
  - id: ollama-route
    uri: /*
    ...
  - id: another-route
    uri: /api/v2/*
    upstream:
      nodes:
        "some-other-service.namespace.svc.cluster.local:8080": 1
      type: roundrobin
#END
```
