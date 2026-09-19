import type {
  PromptRequest,
  EngineeringPrompt,
  PromptAnalysis,
  RequirementAnalysis,
  PromptTransformationResponse,
} from '@ai-assistant/shared-types';

/**
 * Foundational interface for prompt generation engines (M1 + M2 interface).
 */
export interface IPromptEngine {
  analyze(request: PromptRequest): Promise<PromptAnalysis | RequirementAnalysis>;
  formatPrompt(analysis: PromptAnalysis | RequirementAnalysis, context?: unknown): Promise<EngineeringPrompt>;
  validate(prompt: EngineeringPrompt): Promise<boolean>;
  transform?(request: PromptRequest): Promise<PromptTransformationResponse>;
}

export const ENGINE_VERSION = '0.3.0-llm-integration';

export * from '@ai-assistant/shared-types';
