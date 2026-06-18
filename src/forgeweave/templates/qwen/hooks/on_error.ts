/**
 * ForgeWeave on_error hook
 * Logs errors with forge context for debugging.
 */
import { HookContext, HookResponse } from '@qwen/code';

export async function onError(ctx: HookContext): Promise<HookResponse> {
  const { error, sessionId } = ctx;

  await ctx.callTool('forge.memory_write', {
    key: `error:${Date.now()}`,
    value: {
      message: error?.message || 'Unknown error',
      stack: error?.stack,
      session_id: sessionId,
      timestamp: new Date().toISOString(),
    },
    namespace: 'errors',
    ttl_seconds: 604800,
  });

  return { decision: 'allow' };
}
