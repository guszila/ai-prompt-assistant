<script lang="ts">
  import StatusBadge from './StatusBadge.svelte';
  import { appState } from '../stores/appState.svelte';
</script>

<header class="app-header">
  <div class="logo-area">
    <div class="logo-icon">AI</div>
    <div>
      <h1 class="app-title">AI Engineering Assistant</h1>
      <p class="app-subtitle">M1 Foundation Shell</p>
    </div>
  </div>

  <div class="header-actions">
    <div class="service-indicator">
      <span class="indicator-label">AI Service:</span>
      <StatusBadge status={appState.system.aiService.status} />
    </div>
    <button class="refresh-btn" onclick={() => appState.refreshHealth()}>
      Refresh
    </button>
  </div>
</header>

<style>
  .app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
    background-color: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
  }

  .logo-area {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .logo-icon {
    width: 36px;
    height: 36px;
    border-radius: var(--radius);
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
  }

  .app-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .app-subtitle {
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .service-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .indicator-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
  }

  .refresh-btn {
    background-color: var(--bg-tertiary);
    color: var(--text-primary);
    border: 1px solid var(--border);
    padding: 6px 12px;
    border-radius: var(--radius);
    font-size: 0.8rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .refresh-btn:hover {
    background-color: var(--accent);
  }
</style>
