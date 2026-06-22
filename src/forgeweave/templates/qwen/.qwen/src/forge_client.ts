/**
 * ForgeWeave MCP Client for Qwen Extension
 * Provides typed wrappers for forgeweave operations.
 */

export interface ForgeInitInput {
  tui: 'opencode' | 'claude' | 'gemini' | 'qwen';
  project_dir: string;
  overwrite?: boolean;
}

export interface ForgeExecuteCommandInput {
  command: string;
  args?: string;
  context?: Record<string, unknown>;
  job_id?: string;
}

export interface ForgeExecuteSkillInput {
  skill: string;
  params: Record<string, unknown>;
  context?: Record<string, unknown>;
}

export interface ForgeCreateAgentInput {
  agent_id: string;
  role: string;
  tools?: string[];
  skills?: string[];
  constraints?: string;
  temperature?: number;
}

export interface ForgeResearchInput {
  topic: string;
  depth?: 'quick' | 'standard' | 'deep';
  focus?: 'usage' | 'architecture' | 'comparison' | 'general';
  constraints?: string;
  max_sources?: number;
}

export interface ForgeSearchInput {
  query: string;
  max_results?: number;
  source_filter?: string;
}

export interface ForgeLoadContextInput {
  project_dir: string;
}

export interface ForgeValidateInput {
  target: string;
  rules: string[];
}

export interface ForgeMemoryWriteInput {
  key: string;
  value: unknown;
  namespace?: string;
  ttl_seconds?: number;
}

export interface ForgeMemoryReadInput {
  key?: string;
  namespace?: string;
}

export interface ForgeStatusInput {
  job_id: string;
}

export interface ForgeCapabilitiesInput {
  project_dir?: string;
}

export type ForgeToolInput =
  | ForgeInitInput
  | ForgeExecuteCommandInput
  | ForgeExecuteSkillInput
  | ForgeCreateAgentInput
  | ForgeResearchInput
  | ForgeSearchInput
  | ForgeLoadContextInput
  | ForgeValidateInput
  | ForgeMemoryWriteInput
  | ForgeMemoryReadInput
  | ForgeStatusInput
  | ForgeCapabilitiesInput;
