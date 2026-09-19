<script lang="ts">
  import { onMount } from 'svelte';
  import AppLayout from './layouts/AppLayout.svelte';
  import SystemOverview from './features/placeholder/SystemOverview.svelte';
  import { appState } from './stores/appState.svelte';

  onMount(() => {
    appState.refreshHealth();
  });
</script>

<AppLayout>
  <SystemOverview />
</AppLayout>
