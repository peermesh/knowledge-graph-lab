Use Docker Compose + Traefik now, optionally Portainer CE for GUI, and prepare a Helm + Argo CD path for Kubernetes later. This aligns with enterprise practices and your constraints. ([Docker Documentation][1])

# PeerMesh / Knowledge Graph Lab — Deployment Tools Overview

## Scope

* Envs: Dev (macOS), Staging (local Ubuntu), Prod (KVM VPS 12 GB RAM, 8 vCPU).
* Workloads: Dockerized services plus a Chia full node with a long-lived external DB.
* Needs: One-click updates, health-gated rollouts, quick rollback, host-mounted state, scripted per-host init, future-proof to Kubernetes.

## Baseline stack (now)

* **Orchestrator**: Docker Compose as the canonical app spec across envs. Widely used, documented, and stable. ([Docker Documentation][1])
* **Ingress/TLS**: Traefik with the Docker provider. Route via labels, auto-TLS via Let’s Encrypt. ([Traefik Docs][2])
* **Optional management UI**: Portainer CE for stacks, RBAC-lite, registries, webhooks. De facto and familiar to enterprises. ([Portainer Documentation][3])
* **Provisioning**: Ansible playbooks to bootstrap hosts (Docker CE, users, mount points, snapshots). Ansible is standard for repeatable server config. ([Ansible Documentation][4])
* **CI**: GitHub Actions to build, tag, and push images with Buildx. Proven official actions. ([Docker Documentation][5])

## Future path (Kubernetes-ready)

* **Stateful workloads** with **StatefulSets** and PVCs. Sticky identity and ordered rollouts. ([Kubernetes][6])
* **Packaging** with **Helm** following chart best practices and promotion between envs. ([Helm][7])
* **GitOps** with **Argo CD**. Declarative Applications, environment sync, drift control, SSO/RBAC. ([Argo CD][8])

---

## Tool options and when to pick them

### Compose + Traefik (recommended baseline)

* Pattern: single host or small fleet, simple YAML, health-gated start order with `depends_on` + healthchecks. ([Docker Documentation][9])
* Traefik adds standardized routing and automatic certificates via labels. ([Traefik Docs][2])
* Why it fits: fastest path that still reads “enterprise-sane” and maps 1:1 to later Helm values.

### Portainer CE (optional)

* Adds GUI, RBAC features, and stack webhooks over Docker/Swarm/K8s. Easy to demo and audit. ([Portainer Documentation][3])
* Run locally or on the server; no license required for CE. ([Portainer Documentation][10])

### CapRover or Dokku (alternative PaaS layers)

* **CapRover**: Swarm-based, zero-downtime guided by health checks, dashboard + SSL. Good “Heroku-like” flow. ([CapRover][11])
* **Dokku**: Mature single-host PaaS with plugins for DBs, backups, etc.; git-push deploys. ([Dokku][12])
* Pick if you want a platform feel on one server. Otherwise Compose + Traefik is simpler and more portable.

---

## Handling the Chia node state

* **Where the DB lives**: under `$CHIA_ROOT`, default `~/.chia/mainnet/db/`. Make it a host bind mount in staging and prod. ([Chia Documentation][13])
* **Seeding to avoid long syncs**: Chia provides official database torrents; place the DB files into the target `db/` before first start. ([Chia Documentation][14])
* **Relocation**: set `CHIA_ROOT` to move the location cleanly when needed. ([Chia Documentation][13])
* **Backups**: snapshot the mounted DB path from the host with a one-shot container (tar/rsync). Keep dated archives and rotate.

---

## Rollout and rollback mechanics

### Compose specifics

* **Start order and gating**: use `depends_on` with `condition: service_healthy` and per-service `healthcheck` commands; only promote traffic after health passes. ([Docker Documentation][9])
* **Traefik routing**: expose only services with labels; enable ACME/Let’s Encrypt resolver for auto-certs. ([Traefik Docs][2])
* **Immutable images**: tag `app:<env>-<gitsha>-<timestamp>` and keep `app:<env>` as a moving alias. Patterns are common in Docker CI docs. ([Docker Documentation][5])

### CI outline (GitHub Actions)

* Build multi-arch images with Buildx, push to registry, and trigger redeploy. ([Docker Documentation][5])

Minimal workflow excerpt:

```yaml
name: build-and-push
on: { push: { branches: [ main ] } }
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/org/app:prod-${{ github.sha }},ghcr.io/org/app:prod
```

Refs for the actions above. ([GitHub][15])

---

## Provisioning and host setup

* Use **Ansible playbooks** to install Docker CE on Ubuntu 22.04 and create the directory layout for host-mounted volumes (Chia DB, app data). Best-practice playbooks are documented and widely referenced. ([Ansible Documentation][4])
* Official Docker CE install guidance for Ubuntu 22.04 is the baseline for your role. ([Docker Documentation][16])

---

## Security and secrets

* In Compose: keep credentials in env-specific files or Docker/Traefik secrets; prefer secret files when possible. Traefik + labels does not require exposing secret values. ([Traefik Docs][2])
* In CI: store registry and deploy tokens in GitHub Actions secrets per environment. ([GitHub Docs][17])

---

## Backup/restore pattern

* **Volumes and binds**: use a helper container to tar the bind/volume to a dated archive on the host, then offload to object storage if desired.
* **Chia**: stop wallet if necessary, archive `~/.chia/mainnet/db/` and `wallet/` separately; restore to the exact path before service start per Chia docs. ([Chia Documentation][14])

---

## Costs and operations

* **Compose, Traefik, Portainer CE** are free to run. Portainer BE exists if you later need enterprise features and support. ([Portainer Documentation][3])
* All components run locally or on your VPS; no forced cloud dependencies.

---

## Kubernetes track (when needed)

* **Helm**: author one chart per service, parameterize `values.yaml` for dev/staging/prod, and promote the same chart across envs. ([Helm][7])
* **Argo CD**: one `Application` per environment, tracking branches or tags; Argo enforces desired state and supports multi-tenant setups. ([Argo CD][18])

---

## Decision matrix

| Objective                                        | Best fit now                  | Reason                                                                                |
| ------------------------------------------------ | ----------------------------- | ------------------------------------------------------------------------------------- |
| Fastest credible path on one VPS + local staging | Compose + Traefik             | Simple, health-gated rollouts, standard labels, easy TLS. ([Docker Documentation][9]) |
| “Looks enterprise,” web GUI, API                 | + Portainer CE                | Familiar dashboards over Docker/Swarm/K8s. ([Portainer Documentation][3])             |
| Platform feel with push deploys                  | CapRover or Dokku             | Heroku-like, single host friendly. ([CapRover][11])                                   |
| Kubernetes migration                             | Helm + Argo CD + StatefulSets | Standard charting, GitOps, and stateful primitives. ([Helm][7])                       |

---

## Recommended next steps

1. **Lock the baseline**: Compose + Traefik with health-gated services and immutable tags. ([Docker Documentation][9])
2. **Codify hosts**: Ansible role for Docker CE on Ubuntu 22.04 and directory creation for bind mounts, including `CHIA_ROOT`. ([Docker Documentation][16])
3. **Seed Chia properly**: fetch the official DB snapshot and place it under `~/.chia/mainnet/db/` on staging/prod before first start. ([Chia Documentation][14])
4. **Wire CI**: GitHub Actions using Buildx to build/push multi-tag images; tag `prod-<sha>` and `prod`. ([Docker Documentation][5])
5. **Optionally add Portainer CE** for stack webhooks and GUI ops, if stakeholder confidence requires it. ([Portainer Documentation][3])
6. **Prepare K8s path**: skeleton Helm chart + Argo CD `Application` for the same topology. ([Helm][7])

If you want, I will return a concrete repo layout with `compose.yaml`, Traefik labels, an Ansible bootstrap role for Ubuntu 22.04, and a CI workflow matching this plan.

[1]: https://docs.docker.com/reference/compose-file/services/?utm_source=chatgpt.com "Define services in Docker Compose"
[2]: https://doc.traefik.io/traefik/expose/docker/?utm_source=chatgpt.com "Exposing Services with Traefik on Docker"
[3]: https://docs.portainer.io/?utm_source=chatgpt.com "Portainer Documentation: Welcome"
[4]: https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html?utm_source=chatgpt.com "Ansible playbooks — Ansible Community Documentation"
[5]: https://docs.docker.com/build/ci/github-actions/?utm_source=chatgpt.com "Docker Build GitHub Actions"
[6]: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/?utm_source=chatgpt.com "StatefulSets"
[7]: https://helm.sh/docs/chart_best_practices/?utm_source=chatgpt.com "Best Practices"
[8]: https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/?utm_source=chatgpt.com "Declarative Setup - Argo CD - Read the Docs"
[9]: https://docs.docker.com/compose/how-tos/startup-order/?utm_source=chatgpt.com "Control startup and shutdown order with Compose"
[10]: https://docs.portainer.io/start/install-ce/server/kubernetes/baremetal?utm_source=chatgpt.com "Install Portainer CE on your Kubernetes environment"
[11]: https://caprover.com/docs/zero-downtime.html?utm_source=chatgpt.com "Zero Downtime Deployments"
[12]: https://dokku.com/docs/deployment/application-deployment/?utm_source=chatgpt.com "Deploying an Application - Dokku Documentation"
[13]: https://docs.chia.net/reference-client/install-and-setup/installation/?utm_source=chatgpt.com "Advanced Installation | Chia Documentation"
[14]: https://docs.chia.net/reference-client/troubleshooting/node-syncing/?utm_source=chatgpt.com "Node Syncing | Chia Documentation"
[15]: https://github.com/docker/setup-buildx-action?utm_source=chatgpt.com "docker/setup-buildx-action"
[16]: https://docs.docker.com/engine/install/ubuntu/?utm_source=chatgpt.com "Install Docker Engine on Ubuntu"
[17]: https://docs.github.com/actions/guides/publishing-docker-images?utm_source=chatgpt.com "Publishing Docker images"
[18]: https://argo-cd.readthedocs.io/?utm_source=chatgpt.com "Argo CD - Declarative GitOps CD for Kubernetes"
