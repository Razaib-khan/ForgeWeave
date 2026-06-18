"""Extract a selected code block into a new function."""

import argparse
from pathlib import Path


def extract_function(file_path: Path, function_name: str, start_line: int, end_line: int) -> str:
    lines = file_path.read_text().split("\n")
    extracted = lines[start_line - 1 : end_line]
    new_lines = lines[: start_line - 1] + lines[end_line:]

    # Build the new function wrapper
    indent = " " * 4
    body = "\n".join(indent + line for line in extracted)
    new_function = f"def {function_name}():\n{body}\n\n"

    # Write back the original file (with call replaced)
    file_path.write_text("\n".join(new_lines))

    return new_function


def main():
    parser = argparse.ArgumentParser(description="Extract code block into function")
    parser.add_argument("file", type=Path, help="Source file")
    parser.add_argument("--name", required=True, help="New function name")
    parser.add_argument("--start", type=int, required=True, help="Start line")
    parser.add_argument("--end", type=int, required=True, help="End line (inclusive)")
    parser.add_argument(
        "--output", type=Path, help="Output file for extracted function (default: --file)"
    )
    args = parser.parse_args()

    func = extract_function(args.file, args.name, args.start, args.end)
    output = args.output or args.file

    # Prepend the new function to the output file
    existing = output.read_text() if output.exists() else ""
    output.write_text(func + "\n" + existing)
    print(f"Extracted function '{args.name}' from {args.file}:{args.start}-{args.end}")
    print(f"Function:\n{func}")


if __name__ == "__main__":
    main()
