<script lang="ts">
  interface Props {
    status: 'ok' | 'offline' | 'checking';
    label?: string;
  }

  let { status, label }: Props = $props();
</script>

<div class="status-badge status-{status}">
  <span class="dot"></span>
  <span class="text">{label ?? status.toUpperCase()}</span>
</div>

<style>
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }

  .status-ok {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
  }

  .status-ok .dot {
    background-color: #10b981;
    box-shadow: 0 0 8px #10b981;
  }

  .status-offline {
    background-color: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  .status-offline .dot {
    background-color: #ef4444;
  }

  .status-checking {
    background-color: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
  }

  .status-checking .dot {
    background-color: #f59e0b;
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }
</style>
