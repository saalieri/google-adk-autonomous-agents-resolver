# SIMPLE GOOGLE ADK AGENTS SIMULATION
This repository is for testing whether the Discord Server can notify me of new issues in this repo, and whether my Autonomous ADK Agents can analyze those issues and create pull requests.

### Workflow Explanation:

1. **Start** – The automation is triggered.  
2. **New GitHub Issue Appears** – Detects a new issue in the repository.  
3. **My Agents Analyze the Issue and Create PR** – Autonomous agents generate a proposed fix.  
4. **Notify Me** – You receive notifications about the issue and the new PR.  
5. **Waiting for My Approval** – The workflow pauses for your review.  
6. **If Approved → Merged PR** – The PR is merged automatically.  
7. **If Rejected → Back to Agents** – The agents revise and refactor the fix, looping until approved.  
8. **End** – Workflow completes after successful merge.  

# Automated Issue-to-PR Workflow

```mermaid
flowchart TD
    Start([Start])
    NewIssue([New GitHub Issue Appears])
    Analyze([My Agents Analyze the Issue and Create PR for Fix])
    Notify([Notify Me About Issue and New PR])
    Approval([Waiting for My Approval])
    Merge([Merged PR if Approved])
    End([End])

    Start --> NewIssue
    NewIssue --> Analyze
    Analyze --> Notify
    Notify --> Approval
    Approval -->|Approved| Merge
    Approval -->|Rejected| Analyze
    Merge --> End
