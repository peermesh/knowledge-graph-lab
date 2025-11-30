// Entity Extraction UI

const apiBaseUrlInput = document.getElementById("api-base-url");
const inputText = document.getElementById("input-text");
const confidenceThreshold = document.getElementById("confidence-threshold");
const sourceType = document.getElementById("source-type");
const entityTypesInput = document.getElementById("entity-types");
const extractBtn = document.getElementById("extract-btn");
const loading = document.getElementById("loading");
const error = document.getElementById("error");
const jsonOutput = document.getElementById("json-output");
const entitiesList = document.getElementById("entities-list");
const relationshipsList = document.getElementById("relationships-list");
const stats = document.getElementById("stats");
const statEntities = document.getElementById("stat-entities");
const statRelationships = document.getElementById("stat-relationships");
const statTime = document.getElementById("stat-time");

// Tab management
const tabs = document.querySelectorAll(".tab");
const tabContents = document.querySelectorAll(".tab-content");

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        const targetTab = tab.dataset.tab;
        
        // Update active states
        tabs.forEach(t => t.classList.remove("active"));
        tabContents.forEach(tc => tc.classList.remove("active"));
        
        tab.classList.add("active");
        document.getElementById(`${targetTab}-tab`).classList.add("active");
    });
});

// Vis-network setup
const nodes = new vis.DataSet([]);
const edges = new vis.DataSet([]);
const network = new vis.Network(
    document.getElementById("graph-container"),
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

document.getElementById("reset-graph").addEventListener("click", () => {
    if (nodes.length > 0) {
        network.fit({ animation: { duration: 450, easingFunction: "easeInOutQuad" } });
    }
});

network.on("selectNode", (params) => {
    const nodeId = params.nodes[0];
    const meta = nodeMetadata.get(nodeId);
    if (!meta) {
        document.getElementById("graph-info").textContent = "";
        return;
    }

    const infoLines = [
        `<strong>${meta.text}</strong>`,
        meta.type ? `Type: ${meta.type}` : null,
        `Confidence: ${(meta.confidence * 100).toFixed(1)}%`,
        meta.metadata && Object.keys(meta.metadata).length
            ? `Metadata: ${JSON.stringify(meta.metadata, null, 2)}`
            : null
    ].filter(Boolean);

    document.getElementById("graph-info").innerHTML = infoLines.join("<br>");
});

network.on("deselectNode", () => {
    document.getElementById("graph-info").textContent = "";
});

// Extraction function
extractBtn.addEventListener("click", async () => {
    await performExtraction();
});

async function performExtraction() {
    const baseUrl = apiBaseUrlInput.value.trim().replace(/\/$/, "");
    if (!baseUrl) {
        showError("Please provide a valid API base URL.");
        return;
    }

    const text = inputText.value.trim();
    if (!text) {
        showError("Please enter text to extract entities from.");
        return;
    }

    // Prepare request
    const entityTypes = entityTypesInput.value
        .split(",")
        .map(item => item.trim())
        .filter(Boolean);

    const requestData = {
        document_id: generateUUID(),
        content: text,
        document_type: "text",
        extraction_config: {
            confidence_threshold: parseFloat(confidenceThreshold.value) || 0.7,
            source_type: sourceType.value,
            entity_types: entityTypes.length > 0 ? entityTypes : null
        },
        priority: "normal"
    };

    // Show loading state
    setLoadingState(true);
    clearError();
    clearResults();

    try {
        const response = await fetch(`${baseUrl}/ai/v1/extract-entities`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: `HTTP ${response.status}` }));
            throw new Error(errorData.detail || `Request failed with status ${response.status}`);
        }

        const data = await response.json();

        // Handle async job response
        if (data.status === "pending" || data.status === "processing") {
            // Poll for job completion
            await pollJobStatus(baseUrl, data.job_id);
        } else {
            // Synchronous response
            displayResults(data);
        }
    } catch (err) {
        showError(`Extraction failed: ${err.message}`);
        console.error("Extraction error:", err);
    } finally {
        setLoadingState(false);
    }
}

async function pollJobStatus(baseUrl, jobId) {
    const maxAttempts = 60;
    const pollInterval = 2000; // 2 seconds

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
        await new Promise(resolve => setTimeout(resolve, pollInterval));

        try {
            const response = await fetch(`${baseUrl}/ai/v1/jobs/${jobId}`);
            if (!response.ok) {
                throw new Error(`Failed to check job status: ${response.status}`);
            }

            const jobData = await response.json();

            if (jobData.status === "completed") {
                displayResults(jobData);
                return;
            } else if (jobData.status === "failed") {
                throw new Error(jobData.error_message || "Job failed");
            }
            // Continue polling if still processing
        } catch (err) {
            showError(`Failed to check job status: ${err.message}`);
            return;
        }
    }

    showError("Job timed out. Please try again.");
}

function displayResults(data) {
    // Display JSON output
    jsonOutput.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;

    // Display entities
    if (data.entities && data.entities.length > 0) {
        const entitiesHtml = data.entities.map(entity => {
            return `
                <div style="margin-bottom: 1rem; padding: 0.75rem; background: rgba(30, 41, 59, 0.65); border-radius: 8px;">
                    <strong style="color: #38bdf8;">${escapeHtml(entity.text)}</strong>
                    <div style="font-size: 0.85rem; color: rgba(148, 163, 184, 0.9); margin-top: 0.25rem;">
                        Type: ${escapeHtml(entity.type)} | 
                        Confidence: ${(entity.confidence * 100).toFixed(1)}% |
                        ID: ${entity.id}
                    </div>
                    ${entity.metadata && Object.keys(entity.metadata).length > 0
                        ? `<div style="font-size: 0.75rem; color: rgba(148, 163, 184, 0.7); margin-top: 0.25rem;">
                            Metadata: ${JSON.stringify(entity.metadata, null, 2)}
                          </div>`
                        : ''}
                </div>
            `;
        }).join("");
        entitiesList.innerHTML = entitiesHtml;
    } else {
        entitiesList.innerHTML = "<pre>No entities extracted.</pre>";
    }

    // Display relationships
    if (data.relationships && data.relationships.length > 0) {
        const relationshipsHtml = data.relationships.map(rel => {
            const sourceEntity = data.entities?.find(e => e.id === rel.source_entity);
            const targetEntity = data.entities?.find(e => e.id === rel.target_entity);
            
            return `
                <div style="margin-bottom: 1rem; padding: 0.75rem; background: rgba(30, 41, 59, 0.65); border-radius: 8px;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <strong style="color: #38bdf8;">${escapeHtml(sourceEntity?.text || rel.source_entity)}</strong>
                        <span style="color: rgba(148, 163, 184, 0.7);">→</span>
                        <span style="color: #22d3ee; font-weight: 500;">${escapeHtml(rel.relationship_type)}</span>
                        <span style="color: rgba(148, 163, 184, 0.7);">→</span>
                        <strong style="color: #38bdf8;">${escapeHtml(targetEntity?.text || rel.target_entity)}</strong>
                    </div>
                    <div style="font-size: 0.85rem; color: rgba(148, 163, 184, 0.9); margin-top: 0.25rem;">
                        Confidence: ${(rel.confidence * 100).toFixed(1)}% | 
                        ID: ${rel.id}
                    </div>
                    ${rel.evidence
                        ? `<div style="font-size: 0.75rem; color: rgba(148, 163, 184, 0.7); margin-top: 0.25rem; font-style: italic;">
                            Evidence: "${escapeHtml(rel.evidence)}"
                          </div>`
                        : ''}
                </div>
            `;
        }).join("");
        relationshipsList.innerHTML = relationshipsHtml;
    } else {
        relationshipsList.innerHTML = "<pre>No relationships extracted.</pre>";
    }

    // Update stats
    if (data.entities && data.relationships) {
        statEntities.textContent = data.entities.length;
        statRelationships.textContent = data.relationships.length;
        statTime.textContent = data.processing_time_seconds
            ? `${data.processing_time_seconds.toFixed(2)}s`
            : "N/A";
        stats.style.display = "grid";
    }

    // Update graph visualization
    updateGraph(data.entities || [], data.relationships || []);
}

function updateGraph(entities, relationships) {
    // Clear existing data
    nodes.clear();
    edges.clear();
    nodeMetadata.clear();

    if (entities.length === 0) {
        return;
    }

    // Create nodes
    const graphNodes = entities.map((entity, index) => {
        const hue = selectHue(entity.type, index);
        
        nodeMetadata.set(entity.id, {
            text: entity.text,
            type: entity.type,
            confidence: entity.confidence,
            metadata: entity.metadata || {}
        });

        return {
            id: entity.id,
            label: `${entity.text}\n(${entity.type})`,
            group: entity.type,
            value: Math.max(8, Math.round(entity.confidence * 20)),
            color: {
                background: `hsla(${hue}, 70%, 50%, 0.9)`,
                border: `hsla(${hue}, 85%, 60%, 1)`,
                highlight: {
                    background: `hsla(${hue}, 70%, 50%, 1)`,
                    border: `hsla(${hue}, 90%, 70%, 1)`
                }
            },
            title: `${entity.text} (${entity.type})`
        };
    });

    // Create edges
    const graphEdges = relationships.map(rel => {
        return {
            id: rel.id,
            from: rel.source_entity,
            to: rel.target_entity,
            label: `${rel.relationship_type} (${(rel.confidence * 100).toFixed(0)}%)`,
            width: Math.max(1, rel.confidence * 2.5),
            arrows: {
                to: {
                    enabled: true
                }
            }
        };
    });

    // Add to network
    nodes.add(graphNodes);
    edges.add(graphEdges);

    // Fit view
    if (nodes.length > 0) {
        requestAnimationFrame(() => {
            network.fit({ animation: { duration: 500, easingFunction: "easeInOutQuad" } });
        });
    }
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

function setLoadingState(isLoading) {
    extractBtn.disabled = isLoading;
    extractBtn.textContent = isLoading ? "Extracting..." : "Extract Entities";
    loading.classList.toggle("active", isLoading);
}

function showError(message) {
    error.textContent = message;
    error.classList.add("active");
}

function clearError() {
    error.classList.remove("active");
    error.textContent = "";
}

function clearResults() {
    jsonOutput.innerHTML = '<pre>Processing...</pre>';
    entitiesList.innerHTML = '<pre>Processing...</pre>';
    relationshipsList.innerHTML = '<pre>Processing...</pre>';
    stats.style.display = "none";
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

