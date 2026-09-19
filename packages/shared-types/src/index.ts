/**
 * AI Engineering Assistant - Shared Domain Contracts
 * Lightweight type contracts defining system boundaries (M1 + M2).
 */

export type RequirementLanguage = 'th' | 'en' | 'mixed';
export type PromptStatus = 'draft' | 'analyzed' | 'generated' | 'reviewed' | 'approved' | 'rejected';
export type AmbiguitySeverity = 'low' | 'medium' | 'high';

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
 * Structured representation of missing or unclear requirement information.
 */
export interface Ambiguity {
  ambiguityId: string;
  description: string;
  severity: AmbiguitySeverity;
  relatedRequirement: string;
  clarificationQuestion: string;
  isFunctional: boolean;
}

/**
 * Explicitly captured inference derived from user wording.
 */
export interface Assumption {
  assumptionId: string;
  description: string;
  sourceConcept: string;
  requiresConfirmation: boolean;
}

/**
 * Identified software engineering concept.
 */
export interface TechnicalConcept {
  name: string;
  category: string;
  confidence: number;
  sourceTerms: string[];
  isInferred: boolean;
}

/**
 * Normalized representation of user input while preserving the exact original.
 */
export interface NormalizedRequirement {
  originalText: string;
  normalizedText: string;
  detectedLanguage: RequirementLanguage;
  charCount: number;
  wordCount: number;
}

/**
 * Structured analysis of user requirement without requirement fabrication (M2).
 */
export interface RequirementAnalysis {
  requestId: string;
  originalRequirement: string;
  normalizedRequirement: string;
  intent: string;
  requestedActions: string[];
  entities: string[];
  constraints: string[];
  technicalConcepts: TechnicalConcept[];
  expectedOutput?: string;
  ambiguities: Ambiguity[];
  assumptions: Assumption[];
}

/**
 * Identified technical intent, ambiguity, and constraints (M1 backward-compatible).
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
  role?: string;
  objective?: string;
  context?: string;
  requirements?: string[];
  technicalDetails?: string[];
  constraints?: string[];
  expectedOutput?: string;
  acceptanceCriteria?: string[];
  assumptions?: string[];
  clarificationQuestions?: string[];
  rawMarkdown?: string;
  // M1 backward-compatibility fields:
  systemContext?: string;
  roleDefinition?: string;
  taskInstructions?: string;
  technicalConstraints?: string[];
  inputOutputSpecification?: string;
  verificationSteps?: string[];
  version: number;
  status: PromptStatus;
  createdAt: string;
}

/**
 * Validation report for structured prompt and analysis.
 */
export interface PromptValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
  validatedAt: string;
}

/**
 * Complete aggregated response for prompt analysis and generation (M2).
 */
export interface PromptTransformationResponse {
  requestId: string;
  normalized: NormalizedRequirement;
  analysis: RequirementAnalysis;
  prompt: EngineeringPrompt;
  validation: PromptValidationResult;
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
