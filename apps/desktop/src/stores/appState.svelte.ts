import type { SystemStatusState } from '../types';
import { HealthService } from '../services/healthService';

class AppState {
  system = $state<SystemStatusState>({
    aiService: {
      status: 'checking',
      url: 'http://127.0.0.1:8000',
    },
    tauriAvailable: typeof window !== 'undefined' && '__TAURI_INTERNALS__' in window,
    activeMilestone: 'M3 - LLM Integration',
  });

  async refreshHealth(): Promise<void> {
    this.system.aiService.status = 'checking';
    const result = await HealthService.checkAiServiceHealth(this.system.aiService.url);
    this.system.aiService = result;
  }
}

export const appState = new AppState();
