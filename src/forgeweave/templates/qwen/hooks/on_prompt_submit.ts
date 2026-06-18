/**
 * ForgeWeave on_prompt_submit hook
 * Routes /forge-* commands to forge.execute_command.
 * Corresponds to forge.pre_command lifecycle.
 */
import { HookContext, HookResponse } from '@qwen/code';
import { isForgeCommand, parseForgeCommand } from '../src/forge_bridge';

export async function onPromptSubmit(ctx: HookContext): Promise<HookResponse> {
  const { prompt } = ctx;

  if (isForgeCommand(prompt)) {
    const { command, args } = parseForgeCommand(prompt);

    // Execute via forge-mcp
    const result = await ctx.callTool('forge.execute_command', { command, args });

    // Return the result as if the command was executed directly
    return {
      decision: 'allow',
      output: result?.result || 'Command executed.',
    };
  }

  return { decision: 'allow' };
}
