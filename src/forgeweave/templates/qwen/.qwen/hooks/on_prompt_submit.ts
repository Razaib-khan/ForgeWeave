/**
 * ForgeWeave on_prompt_submit hook
 * Routes /forge-* commands to TUI-native command definitions.
 */
import { HookContext, HookResponse } from '@qwen/code';
import { isForgeCommand, parseForgeCommand } from '../src/forge_bridge';

export async function onPromptSubmit(ctx: HookContext): Promise<HookResponse> {
  const { prompt } = ctx;

  if (isForgeCommand(prompt)) {
    const { command, args } = parseForgeCommand(prompt);
    return {
      decision: 'allow',
      output: `Command \`${command}\` will be handled by TUI command definitions.`,
    };
  }

  return { decision: 'allow' };
}
