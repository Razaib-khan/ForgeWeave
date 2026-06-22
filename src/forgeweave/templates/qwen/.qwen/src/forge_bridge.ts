/**
 * ForgeWeave Bridge — Routes /forge-* commands.
 */
import { HookContext } from '@qwen/code';

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
