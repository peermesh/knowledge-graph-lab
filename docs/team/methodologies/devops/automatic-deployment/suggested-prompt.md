Here is a complete deep-research prompt you can hand to another agent.

# DEEP RESEARCH PROMPT: Deployment Tooling for PeerMesh / Knowledge Graph Lab

## ASSIGNMENT METADATA

* **ID:** RES-PEERMESH-DEPLOY-DR-001
* **Role:** Senior DevOps researcher with Docker, Traefik, Portainer, CapRover, Dokku, Kubernetes, Helm, and Argo CD expertise.
* **Decision Owner:** PeerMesh / Knowledge Graph Lab engineering.
* **Target Choice:** Shortlist and rank deployment approaches for dev → staging → prod with upgrade path to Kubernetes.

## CONTEXT TO INTERNALIZE

* Environments: dev on macOS, staging on local Ubuntu host, prod on KVM VPS (12 GB RAM, 8 vCPU, 400 GB SSD, 1 Gbit/s, Ubuntu 22.04).
* Workloads: multiple services in Docker. One service is a **Chia full node** with a large chain DB that must live outside the container and persist across releases. Long initial sync.
* Current pattern: Docker Compose. Desired: one-click update, health-gated rollout, fast rollback, host bind mounts for state, scripted per-host init. Future: Kubernetes with Helm and GitOps.

## PRIMARY RESEARCH QUESTIONS

1. **Compose-first baseline.** What are current best practices for Compose service health gating, startup order, and secrets? Cite exact docs and show minimal examples. ([Docker Documentation][1])
2. **Ingress.** What is the most common, enterprise-credible way to front Compose services with TLS and routing? Compare Traefik’s Docker provider, label patterns, and ACME requirements. Include operational caveats (ports, DNS, storage). ([Traefik Docs][2])
3. **Mgmt layer options.** Compare Portainer CE/BE, CapRover, and Dokku for multi-env Docker ops. Focus on zero-downtime behavior, health-based cutover, rollback paths, RBAC, and webhook triggers. Note which features are CE vs paid. ([Portainer Documentation][3])
4. **Stateful service pattern for Chia.** Document a robust approach to bind-mounting and snapshotting a large blockchain DB with Compose today, and how that maps to K8s StatefulSets later (PVCs, ordered updates). ([Kubernetes][4])
5. **Kubernetes track.** Define a clean migration plan: Helm chart structure per service, environment promotion strategy, and Argo CD GitOps flows. Provide references to upstream best-practices. ([Helm][5])
6. **Security and secrets.** Specify secret handling in Compose now and equivalents in K8s later. Include risks and mitigations. ([Docker Documentation][6])
7. **Rollbacks.** Detail immutable image tagging and rollback mechanics across Compose, Portainer, CapRover, and Dokku. Note any platform constraints that affect RTO. ([Portainer Documentation][3])

## SCOPE OF WORK

* Survey primary documentation for Docker Compose spec and how-tos (startup order, healthchecks, secrets). ([Docker Documentation][7])
* Survey Traefik docs for Docker label routing and ACME. ([Traefik Docs][2])
* Survey Portainer, CapRover, and Dokku docs for deploy, rollback, webhooks, RBAC, and zero-downtime claims. ([Portainer Documentation][3])
* Survey Kubernetes docs for StatefulSets and Helm chart best practices; add one secondary source on real-world chart promotion. ([Kubernetes][4])

## EVALUATION CRITERIA

Score each option 1–5 on:

* **Reliability**: health-gated rollout, zero-downtime semantics, rollback clarity. ([CapRover][8])
* **Security**: secrets handling, surface area, least privilege. ([Docker Documentation][6])
* **Maintainability**: config ergonomics, standard patterns, upstream velocity. ([Docker Documentation][7])
* **Credibility**: alignment with official docs and common enterprise practice (Traefik, Helm, Argo CD). ([Traefik Docs][2])
* **State management**: first-class support for persistent data now and later on K8s. ([Kubernetes][4])
* **Cost**: license and infra needs, CE vs BE deltas. ([Portainer Documentation][3])
* **Path to K8s**: portability of config and parity with Helm values.

## REQUIRED DELIVERABLES

1. **Executive brief** (≤800 words): recommended baseline now and 6-month K8s path.
2. **Decision matrix** comparing:

   * Compose + Traefik only
   * Compose + Traefik + Portainer CE
   * CapRover
   * Dokku
   * Early K8s (Helm + Argo CD)
     Include row-level citations for any claims.
3. **Reference implementation outlines** (snippets, not full repos):

   * **Compose**: healthcheck + `depends_on` pattern, secrets, bind-mount for Chia DB, immutable tags. ([Docker Documentation][1])
   * **Traefik**: Docker labels for routing and ACME resolver config. ([Traefik Docs][2])
   * **Portainer**: how to register a stack and trigger redeploy via webhook (note CE vs BE). ([Portainer Documentation][3])
   * **CapRover**: health-based zero-downtime and rollback behavior. ([CapRover][8])
   * **Dokku**: git-push deploy and backup guidance. ([Dokku][9])
   * **K8s**: StatefulSet YAML skeleton for the Chia node, Helm chart file tree, and Argo CD `Application`. ([Kubernetes][4])
4. **Risk register**: top 10 risks with mitigations.
5. **Migration plan**: stepwise path from Compose to Helm+Argo with parity mapping.
6. **Appendix**: links to all primary sources.

## METHOD AND EVIDENCE RULES

* Prefer primary documentation. Use secondary sources sparingly and label them clearly.
* Every nontrivial claim gets a citation inline.
* Provide minimal, copy-ready snippets tied to cited docs. Do not invent flags that do not exist.
* Call out deprecated or version-specific behaviors (e.g., `depends_on` condition variants). ([Docker Documentation][1])

## DATA TO COLLECT

* Compose: current docs URLs for services, healthchecks, startup order, secrets. ([Docker Documentation][7])
* Traefik: Docker provider labels, ACME requirements, TLS-ALPN and port 443 constraint. ([Traefik Docs][2])
* Portainer: CE vs BE capabilities, stacks, webhooks availability and constraints. ([Portainer Documentation][3])
* CapRover: zero-downtime flow, health check requirement, and Swarm dependency. ([CapRover][8])
* Dokku: deploy flow, backup guidance, plugin ecosystem notes. ([Dokku][9])
* Kubernetes: StatefulSet guarantees and Helm chart practices, plus environment promotion guidance. ([Kubernetes][4])

## OUTPUT FORMAT

Produce a single Markdown document with these sections:

1. Executive Summary
2. Option Profiles (each tool/stack)
3. Decision Matrix (table with scores and citations)
4. Reference Implementation Outlines (code blocks with comments)
5. Risk Register
6. Migration Plan (Compose → Helm+Argo)
7. Appendix: Source Links

## ACCEPTANCE TESTS

* All examples run with current stable versions and match cited docs.
* The decision matrix is reproducible: each score justified with a quote or doc reference.
* The migration plan maps every Compose construct we use now to its Helm/K8s equivalent.
* The Chia node pattern is viable on our hosts and translates to a StatefulSet with PVCs.

## TIMELINE AND DEPTH

* Produce the first complete draft in one pass using only cited sources above.
* Depth target: ~2,500–4,000 words, code snippets included, minimal prose.

**Primary references to start:**

* Docker Compose services and startup order. ([Docker Documentation][7])
* Compose secrets. ([Docker Documentation][6])
* Traefik Docker + ACME. ([Traefik Docs][2])
* Portainer stacks/webhooks (note CE vs BE). ([Portainer Documentation][3])
* CapRover zero-downtime. ([CapRover][8])
* Dokku deploy and backups. ([Dokku][9])
* K8s StatefulSets and Helm best practices. ([Kubernetes][4])

Deliver exactly in the specified format.

[1]: https://docs.docker.com/compose/how-tos/startup-order/?utm_source=chatgpt.com "Control startup and shutdown order with Compose"
[2]: https://doc.traefik.io/traefik/expose/docker/?utm_source=chatgpt.com "Exposing Services with Traefik on Docker"
[3]: https://docs.portainer.io/2.27/user/docker/stacks/webhooks?utm_source=chatgpt.com "Webhooks"
[4]: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/?utm_source=chatgpt.com "StatefulSets"
[5]: https://helm.sh/docs/chart_best_practices/?utm_source=chatgpt.com "Best Practices"
[6]: https://docs.docker.com/compose/how-tos/use-secrets/?utm_source=chatgpt.com "Secrets in Compose | Docker Docs"
[7]: https://docs.docker.com/reference/compose-file/services/?utm_source=chatgpt.com "Define services in Docker Compose"
[8]: https://caprover.com/docs/zero-downtime.html?utm_source=chatgpt.com "Zero Downtime Deployments"
[9]: https://dokku.com/docs/deployment/application-deployment/?utm_source=chatgpt.com "Deploying an Application - Dokku Documentation"
