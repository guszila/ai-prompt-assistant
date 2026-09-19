import type { ServiceHealth } from '../types';

export class HealthService {
  private static defaultUrl = 'http://127.0.0.1:8000';

  public static async checkAiServiceHealth(baseUrl: string = this.defaultUrl): Promise<ServiceHealth> {
    try {
      const response = await fetch(`${baseUrl}/health`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        return {
          status: 'offline',
          url: baseUrl,
          errorMessage: `HTTP ${response.status}: ${response.statusText}`,
          lastChecked: new Date().toISOString(),
        };
      }

      const data = (await response.json()) as { status: string };
      return {
        status: data.status === 'ok' ? 'ok' : 'offline',
        url: baseUrl,
        lastChecked: new Date().toISOString(),
      };
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to reach AI service';
      return {
        status: 'offline',
        url: baseUrl,
        errorMessage: msg,
        lastChecked: new Date().toISOString(),
      };
    }
  }
}
