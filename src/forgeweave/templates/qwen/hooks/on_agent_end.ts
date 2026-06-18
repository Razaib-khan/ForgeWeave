/**
 * ForgeWeave on_agent_end hook
 * Saves agent session output to persistent memory.
 * Corresponds to forge.post_command + forge.post_skill lifecycle.
 */
import { HookContext, HookResponse } from '@qwen/code';

export async function onAgentEnd(ctx: HookContext): Promise<HookResponse> {
  const { output, sessionId } = ctx;

  // Persist agent output to forge memory
  await ctx.callTool('forge.memory_write', {
    key: `agent:session:${sessionId}`,
    value: {
      output: output ? JSON.stringify(output).slice(0, 1000) : null,
      timestamp: new Date().toISOString(),
    },
    namespace: 'agent_sessions',
    ttl_seconds: 604800, // 7 days
  });

  return { decision: 'allow' };
}
