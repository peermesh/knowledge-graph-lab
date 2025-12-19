const form = document.getElementById("query-form");
const apiBaseUrlInput = document.getElementById("api-base-url");
const queryTextInput = document.getElementById("query-text");
const queryTypeSelect = document.getElementById("query-type");
const limitInput = document.getElementById("limit");
const confidenceInput = document.getElementById("confidence");
const entityTypesInput = document.getElementById("entity-types");
const resultsMeta = document.getElementById("results-meta");
const entityList = document.getElementById("entity-list");
const entityTemplate = document.getElementById("entity-template");
const graphContainer = document.getElementById("graph-container");
const graphInfo = document.getElementById("graph-info");
const resetButton = document.getElementById("reset-graph");

// Vis-network setup
const nodes = new vis.DataSet([]);
const edges = new vis.DataSet([]);
const network = new vis.Network(
    graphContainer,
    { nodes, edges },
    {
        physics: {
            stabilization: true,
            barnesHut: {
                gravitationalConstant: -4000,
                centralGravity: 0.3,
                springLength: 120,
                springConstant: 0.04,
                damping: 0.09
            }
        },
        nodes: {
            shape: "dot",
            size: 18,
            font: {
                size: 14,
                face: "Inter",
                align: "center"
            }
        },
        edges: {
            arrows: "to",
            smooth: true,
            font: {
                size: 12,
                strokeWidth: 0,
                align: "horizontal"
            },
            color: {
                color: "rgba(148, 163, 184, 0.65)",
                highlight: "#22d3ee"
            }
        },
        interaction: {
            tooltipDelay: 120,
            hover: true,
            zoomView: true,
            dragView: true
        }
    }
);

const nodeMetadata = new Map();

resetButton.addEventListener("click", () => {
    if (nodes.length > 0) {
        network.fit({ animation: { duration: 450, easingFunction: "easeInOutQuad" } });
    }
});

network.on("selectNode", (params) => {
    const nodeId = params.nodes[0];
    const meta = nodeMetadata.get(nodeId);
    if (!meta) {
        graphInfo.textContent = "";
        return;
    }

    const infoLines = [
        `<strong>${meta.text}</strong>`,
        meta.type ? `Type: ${meta.type}` : null,
        `Confidence: ${(meta.confidence * 100).toFixed(1)}%`,
        meta.metadata && Object.keys(meta.metadata).length
            ? `Metadata: ${JSON.stringify(meta.metadata)}`
            : null
    ].filter(Boolean);

    graphInfo.innerHTML = infoLines.join("<br>");
});

network.on("deselectNode", () => {
    graphInfo.textContent = "";
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    await runQuery();
});

async function runQuery() {
    const baseUrl = apiBaseUrlInput.value.trim().replace(/\/$/, "");
    if (!baseUrl) {
        resultsMeta.textContent = "Please provide a valid API base URL.";
        return;
    }

    const body = {
        query: queryTextInput.value.trim(),
        query_type: queryTypeSelect.value,
        filters: {
            limit: Number(limitInput.value) || 25,
            confidence_threshold: Number(confidenceInput.value) || 0.7
        }
    };

    const entityTypes = entityTypesInput.value
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
    if (entityTypes.length) {
        body.filters.entity_types = entityTypes;
    }

    if (!body.query) {
        resultsMeta.textContent = "Enter a query to search the graph.";
        return;
    }

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

    setLoadingState(true);

    try {
        const response = await fetch(`${baseUrl}/ai/v1/graph/query`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body),
            signal: controller.signal
        });

        clearTimeout(timeout);

        if (!response.ok) {
            const detail = await safeReadJson(response);
            throw new Error(detail?.detail || `Request failed with status ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);
    } catch (error) {
        resultsMeta.textContent = error.name === "AbortError"
            ? "Request timed out after 15 seconds."
            : `Failed to fetch graph data: ${error.message}`;
        clearGraph();
    } finally {
        setLoadingState(false);
    }
}

function setLoadingState(isLoading) {
    form.querySelector("button[type=submit]").disabled = isLoading;
    form.querySelector("button[type=submit]").textContent = isLoading ? "Loading…" : "Run Query";
}

async function safeReadJson(response) {
    try {
        return await response.json();
    } catch {
        return null;
    }
}

function renderResults(data) {
    const { total_results, execution_time_ms, entities } = data;

    resultsMeta.textContent = `${total_results} result${total_results === 1 ? "" : "s"} in ${execution_time_ms} ms`;
    entityList.innerHTML = "";

    const fragment = document.createDocumentFragment();

    if (!Array.isArray(entities) || entities.length === 0) {
        clearGraph();
        return;
    }

    const graphNodes = [];
    const graphEdges = [];
    const presentIds = new Set();

    entities.forEach((entity, index) => {
        presentIds.add(entity.id);
        graphNodes.push(toNode(entity, index));

        const listItem = entityTemplate.content.firstElementChild.cloneNode(true);
        const button = listItem.querySelector(".entity-button");
        const relationshipsContainer = listItem.querySelector(".relationships");

        button.textContent = `${entity.text} · ${entity.type || "Unknown"} · ${(entity.confidence * 100).toFixed(1)}%`;
        button.addEventListener("click", () => focusOnNode(entity.id));

        if (Array.isArray(entity.relationships) && entity.relationships.length) {
            relationshipsContainer.innerHTML = entity.relationships
                .map((rel) => relationshipChip(rel))
                .join("");

            entity.relationships.forEach((rel) => {
                graphEdges.push(toEdge(entity, rel));
                if (!presentIds.has(rel.target_entity_id)) {
                    graphNodes.push(placeholderNode(rel));
                }
            });
        } else {
            relationshipsContainer.textContent = "No relationships in this result.";
        }

        fragment.appendChild(listItem);
    });

    entityList.appendChild(fragment);
    updateGraph(graphNodes, graphEdges);
}

function toNode(entity, index = 0) {
    const hue = selectHue(entity.type, index);
    const label = `${entity.text}\n(${entity.type || "Unknown"})`;

    nodeMetadata.set(entity.id, {
        text: entity.text,
        type: entity.type,
        confidence: entity.confidence,
        metadata: entity.metadata || {}
    });

    return {
        id: entity.id,
        label,
        group: entity.type || "Unknown",
        value: Math.max(8, Math.round(entity.confidence * 20)),
        color: {
            background: `hsla(${hue}, 70%, 50%, 0.9)`,
            border: `hsla(${hue}, 85%, 60%, 1)`,
            highlight: {
                background: `hsla(${hue}, 70%, 50%, 1)`,
                border: `hsla(${hue}, 90%, 70%, 1)`
            }
        },
        title: `${entity.text} (${entity.type || "Unknown"})`
    };
}

function placeholderNode(rel) {
    if (nodeMetadata.has(rel.target_entity_id)) {
        return null;
    }

    nodeMetadata.set(rel.target_entity_id, {
        text: rel.target_entity,
        type: "Related",
        confidence: rel.confidence,
        metadata: {}
    });

    return {
        id: rel.target_entity_id,
        label: `${rel.target_entity}\n(Related)`,
        group: "Related",
        value: Math.max(6, Math.round(rel.confidence * 18)),
        color: {
            background: "rgba(148, 163, 184, 0.35)",
            border: "rgba(148, 163, 184, 0.7)",
            highlight: {
                background: "rgba(148, 163, 184, 0.55)",
                border: "#38bdf8"
            }
        },
        title: `${rel.target_entity} · ${rel.relationship_type}`
    };
}

function toEdge(entity, rel) {
    const from = rel.direction === "incoming" ? rel.target_entity_id : entity.id;
    const to = rel.direction === "incoming" ? entity.id : rel.target_entity_id;
    const id = `${from}:${to}:${rel.relationship_type}`;

    return {
        id,
        from,
        to,
        label: `${rel.relationship_type} (${(rel.confidence * 100).toFixed(0)}%)`,
        width: Math.max(1, rel.confidence * 2.5),
        arrows: {
            to: {
                enabled: true,
                scaleFactor: rel.direction === "incoming" ? 0.8 : 1
            }
        }
    };
}

function relationshipChip(rel) {
    const arrow = rel.direction === "incoming" ? "←" : "→";
    return `<span>${arrow} ${rel.relationship_type} (${(rel.confidence * 100).toFixed(0)}%) → ${rel.target_entity}</span>`;
}

function clearGraph() {
    nodes.clear();
    edges.clear();
    nodeMetadata.clear();
    graphInfo.textContent = "";
}

function updateGraph(graphNodes, graphEdges) {
    const dedupedNodes = graphNodes.filter(Boolean).reduce((acc, node) => {
        acc.set(node.id, node);
        return acc;
    }, new Map());

    const dedupedEdges = graphEdges.reduce((acc, edge) => {
        acc.set(edge.id, edge);
        return acc;
    }, new Map());

    nodes.clear();
    edges.clear();

    nodes.add(Array.from(dedupedNodes.values()));
    edges.add(Array.from(dedupedEdges.values()));

    if (nodes.length > 0) {
        requestAnimationFrame(() => {
            network.fit({ animation: { duration: 500, easingFunction: "easeInOutQuad" } });
        });
    }
}

function focusOnNode(nodeId) {
    if (!nodeId || !nodes.get(nodeId)) {
        return;
    }

    network.selectNodes([nodeId]);
    network.focus(nodeId, {
        scale: 1.2,
        animation: { duration: 400, easingFunction: "easeInOutCubic" }
    });
}

function selectHue(type, index) {
    if (!type) {
        return 210;
    }
    const normalized = type.toLowerCase();
    let hash = 0;
    for (let i = 0; i < normalized.length; i += 1) {
        hash = (hash << 5) - hash + normalized.charCodeAt(i);
        hash |= 0;
    }
    return Math.abs((hash + index * 47) % 360);
}

