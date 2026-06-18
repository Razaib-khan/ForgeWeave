"""Scaffold a new module with standard folder structure."""
import argparse
from pathlib import Path


MODULE_TEMPLATES = {
    "python": {
        "__init__.py": "# {name}\n",
        "{name}.py": "def main():\n    pass\n\n\nif __name__ == '__main__':\n    main()\n",
        "tests/test_{name}.py": "def test_{name}():\n    assert True\n",
    },
    "typescript": {
        "index.ts": "export * from './{name}';\n",
        "{name}.ts": "export function main(): void {\n  // TODO: implement\n}\n",
        "{name}.test.ts": "import { describe, it, expect } from 'vitest';\n\ndescribe('{name}', () => {\n  it('works', () => {\n    expect(true).toBe(true);\n  });\n});\n",
    },
    "node": {
        "index.js": "module.exports = require('./{name}');\n",
        "{name}.js": "function main() {\n  // TODO: implement\n}\n\nmodule.exports = { main };\n",
        "{name}.test.js": "const { describe, it } = require('node:test');\nconst assert = require('node:assert');\n\ndescribe('{name}', () => {\n  it('works', () => {\n    assert.strictEqual(true, true);\n  });\n});\n",
    },
}


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new module")
    parser.add_argument("name", help="Module name")
    parser.add_argument("--lang", choices=list(MODULE_TEMPLATES.keys()), default="python")
    parser.add_argument("--dir", "-d", type=Path, default=Path.cwd(), help="Parent directory")
    args = parser.parse_args()

    module_dir = args.dir / args.name
    module_dir.mkdir(parents=True, exist_ok=True)

    for template_name, template_content in MODULE_TEMPLATES[args.lang].items():
        file_name = template_name.replace("{name}", args.name)
        content = template_content.replace("{name}", args.name)
        file_path = module_dir / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        print(f"  Created {file_path}")

    print(f"\nModule '{args.name}' scaffolded in {module_dir}")


if __name__ == "__main__":
    main()
