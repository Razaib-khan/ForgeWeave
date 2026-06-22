/**
 * ForgeWeave on_error hook
 */
import { HookContext, HookResponse } from '@qwen/code';

export async function onError(ctx: HookContext): Promise<HookResponse> {
  return { decision: 'allow' };
}
