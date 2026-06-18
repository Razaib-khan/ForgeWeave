/**
 * ForgeWeave on_tool_execute hook
 * Validates tool execution against forge rules.
 * Blocks dangerous commands and enforces forge.write lifecycle.
 * Corresponds to forge.pre_file_write + forge.validate hooks.
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

  // Block dangerous bash commands
  if (toolName === 'bash' && toolInput?.command) {
    if (isDangerous(toolInput.command)) {
      return {
        decision: 'block',
        reason: 'Security Policy: Dangerous command detected',
      };
    }
  }

  // Route /forge-* commands through forge.execute_command
  if (toolName === 'bash' && toolInput?.command?.startsWith('/forge-')) {
    const cmd = toolInput.command;
    await ctx.callTool('forge.execute_command', {
      command: cmd.split(/\s+/)[0],
      args: cmd.split(/\s+/).slice(1).join(' '),
    });
    return { decision: 'block', reason: 'Routed through forge.execute_command' };
  }

  return { decision: 'allow' };
}
