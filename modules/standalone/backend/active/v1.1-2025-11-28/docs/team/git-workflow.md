
# Git Workflow Guide for Knowledge Graph Lab

This guide helps you set up Git, create your personal branch, and submit your work to the Knowledge Graph Lab repository. Follow these steps in order to get your development environment ready and make your first contribution.

## Related Documents

- **Phase 1 Deliverables**: [project-plan/phase-1-deliverables.md](project-plan/phase-1-deliverables.md)
- **New to the project?**: Start with [onboarding.md](onboarding.md)

---

## Quick Start (Pick your OS)

**macOS:**
* Install **GitHub Desktop** (includes Git) and **GitHub CLI** (for easy authentication)
* Use Terminal for all commands

**Windows:**
* Install **Git for Windows** (includes Git Bash) and **GitHub CLI**
* Use **Git Bash** for all commands

**Linux (Debian/Ubuntu):**
* `sudo apt install git` and install **GitHub CLI**
* Use your normal shell

> Why this setup? GitHub Desktop provides Git without extra tools. GitHub CLI makes authentication simple across all operating systems.

---

## Install & Authenticate

### macOS

1. **GitHub Desktop**: [https://desktop.github.com/](https://desktop.github.com/)
   * Open once and sign in to GitHub
   * Optional: Desktop → **Preferences → Advanced → Install Command Line Tool** (adds `git` to PATH if needed)

2. **GitHub CLI**: [https://cli.github.com/](https://cli.github.com/) → download the **.pkg** and install

3. **Authenticate** in Terminal:
```bash
gh auth login
# Choose: GitHub.com → HTTPS → Login with web browser
```

4. **Verify installation:**
```bash
git --version
gh --version
```

**Alternative (standalone Git):** Install Git from [https://git-scm.com/download/mac](https://git-scm.com/download/mac), then GitHub CLI as above.

### Windows

1. **Git for Windows** (includes **Git Bash**): [https://gitforwindows.org/](https://gitforwindows.org/)
2. **GitHub CLI**: [https://cli.github.com/](https://cli.github.com/) or via winget: `winget install --id GitHub.cli`
3. **Auth (in Git Bash)**:

```bash
gh auth login
# GitHub.com → HTTPS → Login with web browser
```

4. **Verify:**

```bash
git --version
gh --version
```

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install git
# Install GitHub CLI (official repo)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
  sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
  sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Authenticate
gh auth login
```

---

## Which Shell to Use

* **macOS:** Terminal
* **Windows:** Git Bash (Start Menu → Git Bash)
* **Linux:** Your default shell

> Windows users: Use Git Bash for ALL commands to avoid path issues.

---

## Workspace Setup

Create your project directory:

```bash
cd ~
mkdir -p work/peermesh/knowledge-graph-lab/repo
cd work/peermesh/knowledge-graph-lab/repo
```

> Make sure the `repo` folder is empty before cloning.

---

## Clone & Configure

```bash
git clone https://github.com/peermesh/knowledge-graph-lab.git .
# Set your identity (appears in commits)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## Branch Naming (per-user)

Create a branch using your GitHub username:

```bash
git switch -c yourusername/work   # replace with your GitHub username
```

> **Don't know your GitHub username?** Run `gh api user --jq .login` to see it.

> Use the **same branch** for all your submissions (Phase 1, 2, 3, etc.).

 

---

## Add Your Work & Commit

Navigate to your module folder. Replace `[your-module]` with `backend-architecture`, `frontend-design`, `ai-development`, or `publishing-tools`.

 

### For Phase 1 Research:
```bash
cd docs/team/module-assignments/[your-module]/deliverables/phase-1-research/
# Copy your phase-1-research-brief.md here
git add phase-1-research-brief.md
git commit -m "Add Phase 1 research"
```

### For Phase 2 PRD:
```bash
cd docs/team/module-assignments/[your-module]/deliverables/phase-2-planning/
# Copy your PRD.md here
git add PRD.md
git commit -m "Add Phase 2 PRD: [Your Module]"
```

---

## Push & Open Pull Request

Push your branch to GitHub:

```bash
git push -u origin yourusername/work   # replace with your GitHub username
```

Open a PR (browser):

1. Go to [https://github.com/peermesh/knowledge-graph-lab](https://github.com/peermesh/knowledge-graph-lab)
2. Click **Compare & pull request**
3. Title: `Phase 1 Research - [Your Module]` or `Phase 2 PRD - [Your Module]`
4. Click **Create pull request**
5. Post the PR link in Discord

**OR create PR from CLI:**

```bash
gh pr create --fill
```

---

## Troubleshooting

* **Permission denied / 403:** You don't have repo access. Confirm invite accepted and run `gh auth status`.
* **Branch already exists:** You're probably on it—check with `git branch --show-current`.
* **Nothing to commit:** Verify location with `pwd` and `git status`.
* **Wrong shell on Windows:** Open **Git Bash** and rerun all commands there.
* **Mac prompts for developer tools:** Use GitHub Desktop's **Install Command Line Tool** option or install Git from git-scm.com.
* **Path confusion (Windows):** In Git Bash, `C:\Users\Name` is `/c/Users/Name`.
 

---

## Complete Example

Here's the entire workflow from start to finish:

```bash
# Auth (once per machine)
gh auth login

# Workspace
cd ~
mkdir -p work/peermesh/knowledge-graph-lab/repo
cd work/peermesh/knowledge-graph-lab/repo

# Clone & config
git clone https://github.com/peermesh/knowledge-graph-lab.git .
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create branch
git switch -c yourusername/work   # replace with your GitHub username

# Add file
cd docs/team/module-assignments/backend-architecture/deliverables/phase-1-research/
# (place your phase-1-research-brief.md here)

git add phase-1-research-brief.md
git commit -m "Add Phase 1 research"

# Push
git push -u origin yourusername/work   # replace with your GitHub username

# Open PR (CLI)
gh pr create --fill
```

---

## Team Norms

* **One branch per user**: `username/work`
* **Clear commit messages**: `Add Phase 1 research`
* **PR titles**: `Phase 1 Research - [Module Name]` or `Phase 2 PRD - [Module Name]`
* **Share PR link** in Discord after creating
