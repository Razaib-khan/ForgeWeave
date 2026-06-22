/**
 * ForgeWeave on_tool_execute hook
 * Blocks dangerous shell commands.
 */
import { HookContext, HookResponse } from '@qwen/code';

const DANGEROUS_COMMANDS = [
  /rm\s+.*-[rR]f/,
  /sudo\s+rm/,
  /chmod\s+777/,
  /:\(\s*\{\s*:\|:&\s*\}\s*;/,
];

function isDangerous(command: string): boolean {
  return DANGEROUS_COMMANDS.some(pattern => pattern.test(command));
}

export async function onToolExecute(ctx: HookContext): Promise<HookResponse> {
  const { toolName, toolInput } = ctx;

  if (toolName === 'bash' && toolInput?.command) {
    if (isDangerous(toolInput.command)) {
      return {
        decision: 'block',
        reason: 'Security Policy: Dangerous command detected',
      };
    }
  }

  return { decision: 'allow' };
}
