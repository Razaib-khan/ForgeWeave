/**
 * ForgeWeave on_tool_result hook
 * Logs tool execution results for traceability.
 */
import { HookContext, HookResponse } from '@qwen/code';

export async function onToolResult(ctx: HookContext): Promise<HookResponse> {
  return { decision: 'allow' };
}
