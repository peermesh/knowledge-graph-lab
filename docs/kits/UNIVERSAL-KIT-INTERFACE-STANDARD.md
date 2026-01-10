# Universal Kit Interface Standard (UKIS) v1.0

**Version:** 1.0.0
**Status:** Active
**Last Updated:** 2025-11-15
**Scope:** All kits in the ecosystem

> **See Also:** For bash script patterns, exit codes, and JSON output, see [UKIS-STANDARD.md](/.dev/kits/shared/standards/UKIS-STANDARD.md). This document focuses on CLI flags, directory structure, and metadata schema.

---

## 1. Introduction & Purpose

### What This Is

UKIS defines how all kits behave. When your kit follows UKIS, it works seamlessly with every other kit in the ecosystem.

### Why This Exists

**Problem:** Before UKIS, kits had inconsistent interfaces. Requirements Kit used `--output`, Discovery Kit auto-created directories, and nobody knew what to expect from new kits. This blocked parallel development.

**Solution:** One standard that all kits follow. Now agents can work on different kits simultaneously without coordination.

### What You Get

- **Consistent behavior** - All kits use the same flags and directory patterns
- **Parallel development** - Four agents work on four kits simultaneously without conflicts
- **Auto-validation** - Catch violations before merge
- **Pipeline integration** - Discovery → Requirements → Design works automatically
- **No surprises** - New kits work exactly like existing ones

---

## 2. CLI Interface Standards

### Required Flags

Every kit MUST support:

#### `--help` or `-h`
Show usage and exit.

- Prints help message to stdout
- Exits with code 0
- Does not run kit logic

```bash
./scripts/run-discovery.sh --help
# Shows usage and exits
```

#### `--version`
Show version and exit.

- Prints version number (format: `X.Y.Z`)
- Exits with code 0
- Does not run kit logic

```bash
./scripts/run-discovery.sh --version
# Output: 1.0.0
```

### Prohibited Flags

#### `--output` (NEVER USE THIS)

**Status:** PROHIBITED

**Why:** Bypasses unified directory structure, breaks pipeline integration.

**The Problem:**
```bash
# ❌ Requirements Kit current behavior (wrong)
python -m requirements_kit.cli \
  --discovery-input discovery.json \
  --output /tmp/requirements.md

# Result: Output goes to /tmp/, other kits can't find it
```

**The Fix:**
```bash
# ✅ Use auto-fallback instead
python -m requirements_kit.cli \
  --discovery-input discovery.json

# Result: Auto-creates kit-runs/2025-11-15-09-30-00-RequirementsKit/
#         Output goes to deliverables/ subdirectory
#         Other kits can find it
```

**Why This Matters:**

When Requirements Kit uses `--output`, the Discovery → Requirements pipeline breaks:

1. **No standard location** - Discovery Kit doesn't know where Requirements Kit put files
2. **Broken metadata** - Run tracking can't find outputs
3. **Failed pipelines** - Multi-kit workflows fail to connect stages

### Optional Flags

Kits MAY support:

#### `--verbose` or `-v`
Show detailed output.

- Displays internal processing steps
- Useful for debugging
- Does not change functional behavior

#### `--dry-run`
Preview without executing.

- Shows what would happen
- Validates inputs
- Does not create files or modify state
- Exits with code 0 if validation passes

#### `--debug`
Enable debug-level logging.

- Shows even more detail than `--verbose`
- Includes stack traces
- For troubleshooting only

### Flag Naming Rules

Use kebab-case for all flags:

```bash
# ✅ Correct
--run-dir
--discovery-input
--output-format

# ❌ Wrong
--run_dir      # snake_case not allowed
--runDir       # camelCase not allowed
```

### Flag Behavior Standards

**Boolean flags:**
- Use presence, not value
- Example: `--verbose` (not `--verbose=true`)

**Path flags:**
- Accept absolute or relative paths
- Example: `--run-dir ./my-run` or `--run-dir /absolute/path`

**Required vs optional:**
- Help and version exit immediately
- Other flags run full validation before execution

---

## 3. Directory Structure Requirements

### The Pattern

All kits create outputs in:

```
kit-runs/YYYY-MM-DD-HH-MM-SS-KitName/deliverables/
```

**Components:**
- `kit-runs/` - Fixed prefix
- `YYYY-MM-DD-HH-MM-SS` - Timestamp when kit runs
- `KitName` - Kit identifier (PascalCase)
- `deliverables/` - Where outputs go

**Examples:**
```
kit-runs/2025-11-15-09-30-45-DiscoveryKit/deliverables/
kit-runs/2025-11-15-10-15-22-RequirementsKit/deliverables/
kit-runs/2025-11-15-11-00-00-DesignKit/deliverables/
```

### Full Directory Structure

```
kit-runs/2025-11-15-09-30-45-DiscoveryKit/
├── deliverables/           # Required - all outputs go here
│   ├── discovery-output.json
│   ├── discovery-report.md
│   └── metadata.json       # Required - run metadata
├── logs/                   # Optional - execution logs
│   └── execution.log
└── inputs/                 # Optional - input copies
    └── intake.md
```

**Required:**
- `deliverables/` directory
- `deliverables/metadata.json` file

**Optional:**
- `logs/` directory
- `inputs/` directory

### Auto-Fallback (REQUIRED)

When users don't specify where outputs go, kits MUST auto-create a directory.

**How It Works:**

```bash
# User runs kit without specifying directory
./scripts/run-discovery.sh --input "Build a todo app"

# Kit automatically creates:
kit-runs/2025-11-15-09-30-45-DiscoveryKit/deliverables/

# Kit runs successfully, outputs saved to deliverables/
```

**Why This Is Required:**

- Works without configuration (better user experience)
- Prevents "output path required" errors
- Ensures outputs land in standard location
- Matches behavior users expect

**Current Status:**

- ✅ **Discovery Kit:** Has auto-fallback (compliant)
- ❌ **Requirements Kit:** Missing auto-fallback (needs fixing)

**Requirements Kit Example (Non-Compliant):**

```bash
# ❌ Current behavior - requires --output
python -m requirements_kit.cli \
  --discovery-input discovery.json \
  --output requirements.md

# Without --output, fails with error
```

**Requirements Kit After Fix (Compliant):**

```bash
# ✅ Fixed behavior - auto-creates directory
python -m requirements_kit.cli \
  --discovery-input discovery.json

# Auto-creates: kit-runs/2025-11-15-10-15-22-RequirementsKit/
# Saves to: deliverables/requirements.md
```

### Phase Directory Structure

Each kit creates its own phase directory within the run directory:

- Discovery Kit: `01-discovery/`
- Requirements Kit: `02-requirements/`
- Design Kit: `03-design/`
- Implementation Kit: `04-implementation/`
- Walkthrough Kit: `05-walkthrough/`
- Kickstart Kit: `00-kickstart/` (phase 0 - project setup)

**Standard subdirectories within each phase:**

```
01-discovery/
├── 01-inputs/          # Input files (project descriptions, constraints)
├── 02-process/         # Processing artifacts (logs, intermediate results)
│   ├── logs/           # Execution logs
│   └── artifacts/      # Temporary artifacts
└── 03-deliverables/    # Final outputs (JSON, markdown reports)
```

### Metadata Location

Every run directory MUST contain `run-metadata.json` at the root level.

**Location:** `<run-dir>/run-metadata.json`

**Example:**

```json
{
  "run_id": "2025-11-09-14-30-45",
  "kit_name": "DiscoveryKit",
  "kit_version": "1.0.0",
  "timestamp": "2025-11-09T14:30:45Z",
  "status": "completed",
  "command": "./scripts/run-discovery.sh --input 'Build a todo app'",
  "trigger": "manual",
  "input_source": "inline",
  "module": ""
}
```

---

## Metadata Specifications

All kits must generate metadata that conforms to the kit metadata schema.

### Required Fields

Every kit's `kit-metadata.json` MUST include:

- `name` (string) - Kit name in kebab-case ending with '-kit'
- `version` (string) - Semantic version (e.g., "1.0.0")
- `type` (string) - Kit category: "discovery", "requirements", "design", "implementation", "walkthrough", "kickstart"
- `cli` (object) - CLI specification:
  - `command` (string) - Main CLI command
  - `flags` (object):
    - `required` (array) - Required flags like `["--help", "--version"]`
    - `optional` (array) - Optional flags like `["--verbose", "--debug"]`
    - `prohibited` (array) - Prohibited flags like `["--output"]`
- `timestamp` (string) - ISO 8601 timestamp of metadata creation

### Optional Fields

Kits MAY include:

- `dependencies` (array) - List of kit dependencies (e.g., `["discovery-kit"]`)
- `outputs` (array) - List of output files/directories created by kit
- `description` (string) - Human-readable kit description

### Schema Reference

All metadata must validate against: `schemas/kit-metadata-schema.json`

**Validation command:**

```bash
# Validate kit metadata
python3 -c "
import json, jsonschema
schema = json.load(open('schemas/kit-metadata-schema.json'))
metadata = json.load(open('.dev/kits/discovery-kit/kit-metadata.json'))
jsonschema.validate(metadata, schema)
print('✅ Metadata is valid')
"
```

### Example: Discovery Kit Metadata

```json
{
  "name": "discovery-kit",
  "version": "1.0.0",
  "type": "discovery",
  "cli": {
    "command": "./scripts/run-discovery.sh",
    "flags": {
      "required": ["--help", "--version"],
      "optional": ["--verbose", "--debug", "--dry-run", "--run-dir"],
      "prohibited": ["--output"]
    }
  },
  "timestamp": "2025-11-13T00:00:00Z",
  "dependencies": [],
  "outputs": [
    "01-discovery/03-deliverables/discovery-output.json",
    "01-discovery/03-deliverables/discovery-summary.md"
  ],
  "description": "Universal technology primitive discovery system"
}
```

---

## Execution Lifecycle

All kits must follow a standard execution lifecycle to ensure predictable behavior and proper error handling.

### Pre-Execution Phase

Before running kit logic, kits MUST:

1. **Validate arguments** - Check required flags are present
2. **Check dependencies** - Verify required tools (bash, python, jq) are available
3. **Validate inputs** - Ensure input files exist and are readable
4. **Create run directory** - Either use `--run-dir` or auto-create timestamped directory

**Example (Discovery Kit):**

```bash
# Argument validation
if [ -z "$INPUT_FILE" ]; then
    log_error "Missing required argument: --input"
    usage
    exit $EXIT_INVALID_ARGS
fi

# Dependency check
if ! command -v jq &> /dev/null; then
    log_error "Required dependency 'jq' not found"
    exit $EXIT_DEPENDENCY_FAILED
fi

# Input validation
if [ ! -f "$INPUT_FILE" ] && [ ! -d "$INPUT_FILE" ]; then
    log_error "Input file not found: $INPUT_FILE"
    exit $EXIT_INPUT_VALIDATION
fi
```

### Execution Phase

During execution, kits MUST:

1. **Create run metadata** - Generate initial metadata with `status: "running"`
2. **Create phase directories** - Set up directory structure (`01-inputs/`, `02-process/`, `03-deliverables/`)
3. **Execute kit logic** - Run analysis, generation, or processing
4. **Write outputs** - Save deliverables to `03-deliverables/`
5. **Log execution** - Write logs to `02-process/logs/execution.log`

**Example directory creation (Discovery Kit):**

```bash
# Auto-create or use provided run directory
if [ -n "$RUN_DIR_PROVIDED" ]; then
    run_dir="$RUN_DIR_PROVIDED"
else
    # Auto-fallback: create timestamped directory
    timestamp=$(date +%Y-%m-%d-%H-%M-%S)
    run_dir="kit-runs/${timestamp}-DiscoveryKit"
fi

# Create phase subdirectories
mkdir -p "$run_dir/01-discovery/01-inputs"
mkdir -p "$run_dir/01-discovery/02-process/logs"
mkdir -p "$run_dir/01-discovery/03-deliverables"
```

### Post-Execution Phase

After execution completes (success or failure), kits MUST:

1. **Update metadata** - Change `status` to "completed" or "failed"
2. **Report results** - Print summary with output paths
3. **Exit with appropriate code** - Use standard exit codes

**Example (Requirements Kit):**

```bash
# Update metadata on success
metadata = generate_run_metadata(
    run_id=run_id,
    start_time=start_time,
    end_time=end_time,
    status="completed"
)
save_run_metadata(metadata, output_path)

# Report results
print(f"Requirements Kit Completed Successfully!")
print(f"  Output: {output_path}")
print(f"  Run directory: {run_dir}")

return EXIT_SUCCESS
```

### Error Handling

All errors MUST:

1. **Log clear error messages** - Explain what failed and why
2. **Use standard exit codes** - See Exit Codes section below
3. **Update metadata on failure** - Set `status: "failed"` and include `error` field
4. **Clean up partial outputs** - Remove incomplete deliverables or mark as incomplete

**Standard exit codes:**

- `0` - Success
- `1` - General error
- `2` - Invalid arguments
- `3` - Input validation failed (file not found, invalid JSON)
- `4` - Execution error (kit logic failed)
- `5` - Output generation failed (I/O error)
- `6` - Dependency check failed (missing required tool)

**Example error handling (Requirements Kit):**

```python
except FileNotFoundError as e:
    logger.error(f"File error: {e}")
    # Save failure metadata
    metadata = generate_run_metadata(
        run_id=run_id,
        start_time=start_time,
        end_time=datetime.utcnow(),
        status="failed",
        error=str(e)
    )
    save_run_metadata(metadata, output_path)
    return EXIT_INPUT_VALIDATION
```

---

## How to Validate Compliance

Use the validation script to check if a kit follows UKIS v1.0.

### Validation Command

```bash
# Validate a kit
./scripts/validate-kit-compliance.sh <kit-directory>

# Examples
./scripts/validate-kit-compliance.sh .dev/kits/discovery-kit
./scripts/validate-kit-compliance.sh .dev/kits/requirements-kit
```

### Exit Codes

- `0` - All checks passed (kit is compliant)
- `1` - One or more checks failed (kit is non-compliant)
- `2` - Warnings detected (kit mostly compliant but has issues)

### What Gets Validated

The validation script checks:

1. **File existence** - `kit-metadata.json`, `README.md`, main script exist
2. **Metadata validation** - Metadata is valid JSON and validates against schema
3. **CLI flag compliance** - No prohibited flags (like `--output`), required flags present
4. **Directory structure** - Required directories exist (`scripts/`, `templates/`)
5. **Execution lifecycle** - `--help` and `--version` flags work

### Example Output

```
✅ [PASS] kit-metadata.json exists
✅ [PASS] Metadata is valid JSON
✅ [PASS] Metadata validates against schema
❌ [FAIL] Prohibited flag detected: --output in cli.py
   Fix: Remove --output flag from requirements_kit/cli.py
   Example: Use --run-dir instead for output location
⚠️  [WARN] README.md is short (only 15 lines)
   Info: Consider adding usage examples and troubleshooting guide

Validation Result: FAILED (1 error, 1 warning)
Exit code: 1
```

### CI/CD Integration

Add the validation script to your CI/CD pipeline to enforce compliance:

**GitHub Actions example:**

```yaml
name: Validate Kits
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Discovery Kit
        run: ./scripts/validate-kit-compliance.sh .dev/kits/discovery-kit
      - name: Validate Requirements Kit
        run: ./scripts/validate-kit-compliance.sh .dev/kits/requirements-kit
```

**Pre-commit hook example:**

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate all kits before commit
for kit_dir in .dev/kits/*/; do
    if [ -f "$kit_dir/kit-metadata.json" ]; then
        echo "Validating $(basename "$kit_dir")..."
        ./scripts/validate-kit-compliance.sh "$kit_dir" || exit 1
    fi
done

echo "✅ All kits passed UKIS validation"
```

### Enforcement Policy

- **Pre-merge:** All kits MUST pass validation (exit code 0) before merging to main
- **Warnings (exit code 2):** Can be merged but should be addressed soon
- **Failures (exit code 1):** Block merge until issues are resolved

---

## Versioning & Evolution

UKIS follows semantic versioning to manage changes over time.

### Version Format

**Format:** `UKIS vX.Y`

- **Major version (X):** Breaking changes to interface contracts
- **Minor version (Y):** Non-breaking additions or clarifications

**Current version:** UKIS v1.0

### Breaking Changes

Changes that increment the major version (v1.0 → v2.0):

- Removing required flags
- Changing directory structure patterns
- Removing required metadata fields
- Changing exit code meanings

**Example breaking change:**

```
UKIS v1.0: Run directory pattern is kit-runs/YYYY-MM-DD-HH-MM-SS-KitName/
UKIS v2.0: Run directory pattern changes to runs/KitName-YYYY-MM-DD/
           → Breaking change, requires kit updates
```

### Non-Breaking Changes

Changes that increment the minor version (v1.0 → v1.1):

- Adding optional flags
- Adding optional metadata fields
- Clarifying documentation
- Adding validation checks that don't fail existing compliant kits

**Example non-breaking change:**

```
UKIS v1.0: No --config flag
UKIS v1.1: Add optional --config flag for configuration files
           → Non-breaking, kits work without it
```

### Deprecation Policy

Before removing features, UKIS provides advance notice:

1. **Deprecation announcement** - Feature marked as deprecated in current version
2. **Grace period** - Feature remains functional for at least 2 minor versions
3. **Removal** - Feature removed in next major version

**Example deprecation:**

```
UKIS v1.0: --output flag is prohibited
UKIS v1.1: (no change)
UKIS v1.2: (no change)
UKIS v2.0: --output flag formally documented as never supported in v1.x
```

### Version Compatibility

Kits MUST declare which UKIS version they comply with in their metadata:

```json
{
  "name": "discovery-kit",
  "version": "1.0.0",
  "ukis_version": "1.0",
  "type": "discovery",
  ...
}
```

### Upgrading to New UKIS Versions

When UKIS releases a new version:

1. Review the changelog for breaking changes
2. Update kit implementation if needed
3. Update `ukis_version` in kit metadata
4. Validate compliance with new version
5. Update documentation and examples

---

## Real-World Examples

### Example 1: Discovery Kit (Compliant)

**Compliance status:** ✅ Mostly compliant (minor file count warnings)

**What it does right:**

1. **Auto-fallback behavior:**
   ```bash
   ./scripts/run-discovery.sh --input "Build a todo app"
   # Auto-creates: kit-runs/2025-11-09-14-30-45-DiscoveryKit/
   ```

2. **Unified directory structure:**
   ```
   kit-runs/2025-11-09-14-30-45-DiscoveryKit/
   ├── 01-discovery/
   │   ├── 01-inputs/
   │   ├── 02-process/
   │   └── 03-deliverables/
   └── run-metadata.json
   ```

3. **Required flags:**
   ```bash
   ./scripts/run-discovery.sh --help     # ✅ Works
   ./scripts/run-discovery.sh --version  # ✅ Works
   ```

4. **No prohibited flags:**
   - No `--output` flag that bypasses directory structure

**Minor issues:**

- File count warnings in console output (cosmetic, not functional)

### Example 2: Requirements Kit (Non-Compliant)

**Compliance status:** ❌ Non-compliant (2 MAJOR issues)

**Issue 1: --output flag bypasses unified directory**

```bash
# ❌ Current behavior (non-compliant)
python -m requirements_kit.cli --discovery-input discovery.json --output /tmp/requirements.md

# ✅ Required behavior (compliant)
python -m requirements_kit.cli --discovery-input discovery.json --run-dir kit-runs/2025-11-09-15-00-12-MyProject/
```

**Why this breaks integration:**

```bash
# Full pipeline (Discovery → Requirements)
./scripts/run-discovery.sh --input "Build a todo app" --run-dir kit-runs/my-project/

# ❌ Requirements Kit can bypass the shared directory
python -m requirements_kit.cli --discovery-input kit-runs/my-project/01-discovery/03-deliverables/discovery-output.json --output /tmp/requirements.md
# Result: Requirements output is in /tmp/, not in kit-runs/my-project/02-requirements/

# ✅ Requirements Kit should use shared directory
python -m requirements_kit.cli --discovery-input kit-runs/my-project/01-discovery/03-deliverables/discovery-output.json --run-dir kit-runs/my-project/
# Result: Requirements output is in kit-runs/my-project/02-requirements/requirements.md
```

**Issue 2: Missing auto-fallback behavior**

```bash
# ❌ Current behavior (non-compliant) - requires explicit --output
python -m requirements_kit.cli --discovery-input discovery.json --output requirements.md
# Error if --output not provided

# ✅ Required behavior (compliant) - auto-creates directory
python -m requirements_kit.cli --discovery-input discovery.json
# Auto-creates: kit-runs/2025-11-09-15-00-12-RequirementsKit/02-requirements/requirements.md
```

**How to fix:**

1. Remove `--output` flag from CLI
2. Add auto-fallback logic (like Discovery Kit has)
3. Use `--run-dir` for shared pipeline runs
4. Auto-create timestamped directory when `--run-dir` not provided

---

## Summary

UKIS v1.0 defines the interface contracts that enable parallel kit development.

**Key requirements:**

- ✅ Support `--help` and `--version` flags
- ❌ No `--output` flag (bypasses unified directory)
- ✅ Auto-create timestamped run directory if `--run-dir` not provided
- ✅ Use phase directories: `01-discovery/`, `02-requirements/`, etc.
- ✅ Generate `run-metadata.json` in run directory root
- ✅ Follow standard execution lifecycle (pre-execution, execution, post-execution)
- ✅ Use standard exit codes (0=success, 2=invalid args, 3=validation failed, etc.)
- ✅ Validate compliance with `./scripts/validate-kit-compliance.sh`

**Benefits:**

- Parallel development (multiple agents, no conflicts)
- Pipeline integration (Discovery → Requirements → Design → Implementation)
- Automated validation (catch violations before merge)
- Consistent user experience (all kits behave the same)

**Questions?**

See the validation script for implementation examples: `scripts/validate-kit-compliance.sh`

See the metadata schema for complete specifications: `schemas/kit-metadata-schema.json`

---

**UKIS v1.0** - Universal Kit Interface Standardization
**Maintained by:** Design Kit Ecosystem Team
**Status:** Active
