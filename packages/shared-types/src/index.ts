/**
 * AI Engineering Assistant - Shared Domain Contracts
 * Lightweight type contracts defining system boundaries (M1).
 */

export type RequirementLanguage = 'th' | 'en';
export type PromptStatus = 'draft' | 'analyzed' | 'generated' | 'reviewed' | 'approved' | 'rejected';

/**
 * Incoming natural language requirement from user.
 */
export interface PromptRequest {
  id: string;
  rawText: string;
  language: RequirementLanguage;
  projectContextId?: string;
  metadata?: Record<string, unknown>;
  createdAt: string;
}

/**
 * Identified technical intent, ambiguity, and constraints.
 */
export interface PromptAnalysis {
  requestId: string;
  identifiedIntent: string;
  technicalDomain: string;
  ambiguities: string[];
  extractedConstraints: string[];
  assumptions: string[];
  suggestedClarifications: string[];
}

/**
 * Structured engineering prompt optimized for AI coding agents.
 */
export interface EngineeringPrompt {
  id: string;
  requestId: string;
  title: string;
  systemContext: string;
  roleDefinition: string;
  taskInstructions: string;
  technicalConstraints: string[];
  inputOutputSpecification: string;
  verificationSteps: string[];
  version: number;
  status: PromptStatus;
  createdAt: string;
}

/**
 * User feedback, ratings, or manual revisions.
 */
export interface PromptFeedback {
  id: string;
  promptId: string;
  rating?: number; // 1-5 scale
  userComment?: string;
  revisedPromptContent?: string;
  isAccepted: boolean;
  createdAt: string;
}

/**
 * Project context metadata (tech stack, coding standards).
 */
export interface ProjectContext {
  id: string;
  name: string;
  techStack: string[];
  codingRules: string[];
  constraints: string[];
  updatedAt: string;
}

/**
 * Session or conversation context.
 */
export interface Conversation {
  id: string;
  title: string;
  projectContextId?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Collected experience record for future learning/evaluation pipeline.
 */
export interface Experience {
  id: string;
  requestId: string;
  promptId: string;
  feedbackId?: string;
  isCurated: boolean;
  createdAt: string;
}

/**
 * Evaluation benchmark result.
 */
export interface EvaluationResult {
  id: string;
  promptId: string;
  metricName: string;
  score: number;
  details?: Record<string, unknown>;
  evaluatedAt: string;
}

/**
 * LLM model version and provider metadata.
 */
export interface ModelVersion {
  id: string;
  provider: string;
  modelIdentifier: string;
  isLocal: boolean;
  active: boolean;
}
