export interface ServiceHealth {
  status: 'ok' | 'offline' | 'checking';
  url: string;
  lastChecked?: string;
  errorMessage?: string;
}

export interface SystemStatusState {
  aiService: ServiceHealth;
  tauriAvailable: boolean;
  activeMilestone: string;
}
