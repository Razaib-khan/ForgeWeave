/**
 * ForgeWeave on_agent_start hook
 * Loads forge context before every agent interaction.
 * Corresponds to forge.pre_command + forge.pre_skill lifecycle.
 */
import { HookContext, HookResponse } from '@qwen/code';

export async function onAgentStart(ctx: HookContext): Promise<HookResponse> {
  // Load project context into the agent
  const context = await ctx.callTool('forge.load_context', {
    project_dir: process.cwd(),
  });

  return {
    decision: 'allow',
    context: {
      forge: context?.result || { status: 'not_initialized' },
      timestamp: new Date().toISOString(),
    },
  };
}
