<script lang="ts">
  import type { Snippet } from 'svelte';
  import Header from '../components/Header.svelte';

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();
</script>

<div class="layout-root">
  <Header />
  <main class="main-content">
    {@render children?.()}
  </main>
  <footer class="app-footer">
    <span>AI Engineering Assistant © 2026 • Foundation Architecture M1</span>
    <span class="tech-stack">Tauri 2 • Svelte 5 • Strict TypeScript • FastAPI</span>
  </footer>
</div>

<style>
  .layout-root {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .main-content {
    flex: 1;
    background-color: var(--bg-primary);
  }

  .app-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 24px;
    background-color: var(--bg-secondary);
    border-top: 1px solid var(--border);
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .tech-stack {
    font-family: monospace;
  }
</style>
