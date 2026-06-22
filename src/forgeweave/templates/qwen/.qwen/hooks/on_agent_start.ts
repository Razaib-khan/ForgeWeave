/**
 * ForgeWeave on_agent_start hook
 */
import { HookContext, HookResponse } from '@qwen/code';

export async function onAgentStart(ctx: HookContext): Promise<HookResponse> {
  return { decision: 'allow' };
}
