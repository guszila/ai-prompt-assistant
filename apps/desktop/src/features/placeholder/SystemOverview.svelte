<script lang="ts">
  import { appState } from '../../stores/appState.svelte';
  import StatusBadge from '../../components/StatusBadge.svelte';
</script>

<div class="overview-container">
  <div class="welcome-card">
    <h2>Foundation Verified</h2>
    <p class="desc">
      AI Engineering Assistant desktop application shell is active. This milestone establishes the modular architectural boundary between Desktop, AI Service, and Infrastructure.
    </p>
  </div>

  <div class="grid">
    <div class="status-card">
      <div class="card-header">
        <h3>AI Service Backend</h3>
        <StatusBadge status={appState.system.aiService.status} />
      </div>
      <p class="url-text">{appState.system.aiService.url}/health</p>
      {#if appState.system.aiService.errorMessage}
        <p class="error-text">{appState.system.aiService.errorMessage}</p>
      {/if}
      <p class="note">Python 3.13 + FastAPI service for prompt transformation & agent boundaries.</p>
    </div>

    <div class="status-card">
      <div class="card-header">
        <h3>Desktop Core</h3>
        <span class="pill">Tauri 2 + Svelte 5</span>
      </div>
      <p class="info-line">Native Shell: {appState.system.tauriAvailable ? 'Tauri Runtime' : 'Web View / Dev Host'}</p>
      <p class="note">Decoupled UI architecture. Zero direct database or LLM provider coupling.</p>
    </div>

    <div class="status-card">
      <div class="card-header">
        <h3>Local Database</h3>
        <span class="pill">SQLite Embedded</span>
      </div>
      <p class="info-line">Local File: data/app.db</p>
      <p class="note">Self-contained desktop persistence. Zero external database server or Docker required.</p>
    </div>

    <div class="status-card">
      <div class="card-header">
        <h3>Current Phase</h3>
        <span class="pill active-pill">{appState.system.activeMilestone}</span>
      </div>
      <p class="info-line">Phase M3: Core Prompt Engine + LLM Integration</p>
      <p class="note">M2 deterministic baseline preserved. LLM enhancement layer with GroundingReconciler and fallback active.</p>
    </div>
  </div>
</div>

<style>
  .overview-container {
    max-width: 960px;
    margin: 0 auto;
    padding: 32px 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .welcome-card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
  }

  .welcome-card h2 {
    font-size: 1.4rem;
    margin-bottom: 8px;
    color: var(--text-primary);
  }

  .desc {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.6;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
    gap: 20px;
  }

  .status-card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .card-header h3 {
    font-size: 1rem;
    color: var(--text-primary);
  }

  .pill {
    background-color: var(--bg-tertiary);
    color: var(--text-secondary);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .active-pill {
    background-color: rgba(59, 130, 246, 0.2);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.3);
  }

  .url-text {
    font-family: monospace;
    font-size: 0.85rem;
    color: var(--text-muted);
  }

  .info-line {
    font-size: 0.88rem;
    color: var(--text-primary);
  }

  .error-text {
    font-size: 0.8rem;
    color: var(--danger);
  }

  .note {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: auto;
  }
</style>
