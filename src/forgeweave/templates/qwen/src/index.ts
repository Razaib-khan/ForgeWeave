/**
 * ForgeWeave Qwen Extension Entry Point
 * Registers all hooks and initializes the framework bridge.
 */
import { ExtensionContext } from '@qwen/code';
import { onAgentStart } from '../hooks/on_agent_start';
import { onAgentEnd } from '../hooks/on_agent_end';
import { onToolExecute } from '../hooks/on_tool_execute';
import { onToolResult } from '../hooks/on_tool_result';
import { onPromptSubmit } from '../hooks/on_prompt_submit';
import { onError } from '../hooks/on_error';

export function activate(context: ExtensionContext) {
  context.registerHook('on_agent_start', onAgentStart);
  context.registerHook('on_agent_end', onAgentEnd);
  context.registerHook('on_tool_execute', onToolExecute);
  context.registerHook('on_tool_result', onToolResult);
  context.registerHook('on_prompt_submit', onPromptSubmit);
  context.registerHook('on_error', onError);

  context.console.info('[ForgeWeave] Extension activated');
}
