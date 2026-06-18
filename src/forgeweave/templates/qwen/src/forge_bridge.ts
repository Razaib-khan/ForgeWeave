/**
 * ForgeWeave Bridge — Routes Qwen events to forge-mcp tools.
 */
import { HookContext } from '@qwen/code';

const FORGE_TOOLS = new Set([
  'forge.init', 'forge.execute_command', 'forge.execute_skill',
  'forge.create_agent', 'forge.research', 'forge.search',
  'forge.load_context', 'forge.validate', 'forge.memory_read',
  'forge.memory_write', 'forge.status', 'forge.capabilities',
]);

export function isForgeTool(name: string): boolean {
  return FORGE_TOOLS.has(name);
}

export function isForgeCommand(prompt: string): boolean {
  return prompt.trim().startsWith('/forge-');
}

export function parseForgeCommand(prompt: string): { command: string; args: string } {
  const parts = prompt.trim().split(/\s+/);
  return {
    command: parts[0],
    args: parts.slice(1).join(' '),
  };
}
