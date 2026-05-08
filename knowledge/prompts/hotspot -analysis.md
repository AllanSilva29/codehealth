# Hotspot Analysis Prompt

Identify high-risk hotspots using:

- git churn
- complexity
- contributor count
- rollback frequency
- temporal coupling

Rules:
- prioritize frequently modified complex files
- reduce severity for stable legacy modules
- identify socio-technical risks

Output:
- ranked hotspots
- hotspot score
- contributing factors
- recommended actions