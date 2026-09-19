import type { PromptRequest, EngineeringPrompt, PromptAnalysis } from '@ai-assistant/shared-types';

/**
 * Foundational interface for prompt generation engines (M1 interface only).
 */
export interface IPromptEngine {
  analyze(request: PromptRequest): Promise<PromptAnalysis>;
  formatPrompt(analysis: PromptAnalysis, context?: unknown): Promise<EngineeringPrompt>;
  validate(prompt: EngineeringPrompt): Promise<boolean>;
}

export const ENGINE_VERSION = '0.1.0-foundation';
