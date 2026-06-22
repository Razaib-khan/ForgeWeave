/**
 * ForgeWeave on_agent_end hook
 */
import { HookContext, HookResponse } from '@qwen/code';

export async function onAgentEnd(ctx: HookContext): Promise<HookResponse> {
  return { decision: 'allow' };
}
