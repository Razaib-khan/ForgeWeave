/**
 * ForgeWeave on_tool_result hook
 * Logs tool execution results for traceability.
 */
import { HookContext, HookResponse } from '@qwen/code';

export async function onToolResult(ctx: HookContext): Promise<HookResponse> {
  const { toolName, result, sessionId } = ctx;

  await ctx.callTool('forge.memory_write', {
    key: `trace:tool:${toolName}:${Date.now()}`,
    value: {
      tool: toolName,
      status: result ? 'success' : 'failure',
      session_id: sessionId,
      timestamp: new Date().toISOString(),
    },
    namespace: 'tool_traces',
    ttl_seconds: 2592000,
  });

  return { decision: 'allow' };
}
