#!/usr/bin/env python3
"""Project-specific structural lint inspired by the supplied Clean Code heuristics.

This complements Ruff with checks that are specific to this refactor: no runtime package
installation, no blanket warning suppression, correct method binding, bounded line length,
and review warnings for broad exceptions, large functions, and parameter-heavy APIs.
"""

from __future__ import annotations

import ast
import builtins
import symtable
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = (ROOT / "src", ROOT / "experiments", ROOT / "tests", ROOT / "scripts")
MAX_LINE_LENGTH = 100
REVIEW_ARGUMENT_THRESHOLD = 5
REVIEW_FUNCTION_LINES = 120



def _symbol_errors(text: str, path: Path) -> list[str]:
    errors: list[str] = []
    table = symtable.symtable(text, str(path), "exec")
    module_names = {symbol.get_name() for symbol in table.get_symbols()}
    builtin_names = set(dir(builtins))

    def visit(child):
        for symbol in child.get_symbols():
            name = symbol.get_name()
            if symbol.is_global() and symbol.is_referenced():
                if name not in module_names and name not in builtin_names:
                    errors.append(
                        f"{path}:{child.get_lineno()}: unresolved global name {name!r}"
                    )
        for grandchild in child.get_children():
            visit(grandchild)

    for child in table.get_children():
        visit(child)
    return errors



def _unused_import_errors(tree: ast.AST, path: Path) -> list[str]:
    """Return conservative F401-style errors for top-level imports."""
    used_names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    exported_names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        has_all_target = any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        )
        if not has_all_target:
            continue
        if isinstance(node.value, (ast.List, ast.Tuple)):
            exported_names.update(
                element.value
                for element in node.value.elts
                if isinstance(element, ast.Constant) and isinstance(element.value, str)
            )

    errors: list[str] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            continue
        if isinstance(node, ast.Import):
            names = [
                (alias.asname or alias.name.split(".")[0], node.lineno)
                for alias in node.names
            ]
        elif isinstance(node, ast.ImportFrom):
            names = [(alias.asname or alias.name, node.lineno) for alias in node.names]
        else:
            continue
        for name, line_number in names:
            if name == "*" or name in used_names or name in exported_names:
                continue
            errors.append(f"{path}:{line_number}: unused import {name!r}")
    return errors

def _decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    names: set[str] = set()
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name):
            names.add(decorator.id)
        elif isinstance(decorator, ast.Attribute):
            names.add(decorator.attr)
    return names


def _argument_count(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    args = node.args
    positional = [*args.posonlyargs, *args.args]
    if positional and positional[0].arg in {"self", "cls"}:
        positional = positional[1:]
    return len(positional) + len(args.kwonlyargs)


def _is_blanket_warning_suppression(node: ast.Call) -> bool:
    if not isinstance(node.func, ast.Attribute):
        return False
    if node.func.attr != "filterwarnings" or not node.args:
        return False
    action = node.args[0]
    ignores_warnings = isinstance(action, ast.Constant) and action.value == "ignore"
    has_category = any(keyword.arg == "category" for keyword in node.keywords)
    return ignores_warnings and not has_category


def _method_binding_errors(class_node: ast.ClassDef, path: Path) -> list[str]:
    errors: list[str] = []
    for node in class_node.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        decorators = _decorator_names(node)
        positional = [*node.args.posonlyargs, *node.args.args]
        first_arg = positional[0].arg if positional else None
        if "staticmethod" in decorators:
            continue
        if "classmethod" in decorators:
            if first_arg != "cls":
                errors.append(
                    f"{path}:{node.lineno}: classmethod {node.name!r} should receive cls first"
                )
            continue
        if first_arg != "self":
            errors.append(
                f"{path}:{node.lineno}: method {node.name!r} is missing self or @staticmethod"
            )
    return errors


def lint_file(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    for line_number, line in enumerate(lines, start=1):
        if "\t" in line:
            errors.append(f"{path}:{line_number}: tab character")
        if line.rstrip() != line:
            errors.append(f"{path}:{line_number}: trailing whitespace")
        if len(line) > MAX_LINE_LENGTH:
            errors.append(
                f"{path}:{line_number}: line length {len(line)} > {MAX_LINE_LENGTH}"
            )

    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        errors.append(f"{path}:{exc.lineno}: syntax error: {exc.msg}")
        return errors, warnings

    errors.extend(_symbol_errors(text, path))
    errors.extend(_unused_import_errors(tree, path))

    seen_top_level_names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in seen_top_level_names:
                errors.append(f"{path}:{node.lineno}: duplicate top-level name {node.name!r}")
            seen_top_level_names.add(node.name)
        if isinstance(node, ast.ClassDef):
            errors.extend(_method_binding_errors(node, path))

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and any(alias.name == "*" for alias in node.names):
            errors.append(f"{path}:{node.lineno}: wildcard import")
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            errors.append(f"{path}:{node.lineno}: bare except")
        if isinstance(node, ast.ExceptHandler) and isinstance(node.type, ast.Name):
            if node.type.id == "Exception":
                warnings.append(
                    f"{path}:{node.lineno}: broad Exception handler; verify this is an API boundary"
                )
        if isinstance(node, ast.Call) and _is_blanket_warning_suppression(node):
            errors.append(f"{path}:{node.lineno}: blanket warnings.filterwarnings('ignore')")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            arg_count = _argument_count(node)
            if arg_count > REVIEW_ARGUMENT_THRESHOLD:
                warnings.append(
                    f"{path}:{node.lineno}: {node.name} has {arg_count} arguments; review F1"
                )
            if node.end_lineno and node.end_lineno - node.lineno + 1 > REVIEW_FUNCTION_LINES:
                warnings.append(
                    f"{path}:{node.lineno}: {node.name} spans "
                    f"{node.end_lineno - node.lineno + 1} lines; review abstraction level"
                )

    forbidden_names = {"pip_install", "install_required_packages"}
    for node in tree.body:
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name in forbidden_names
        ):
            errors.append(
                f"{path}:{node.lineno}: runtime package installation helper {node.name!r}"
            )

    return errors, warnings


def main() -> int:
    python_files = sorted(
        path
        for root in SOURCE_ROOTS
        for path in root.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    errors: list[str] = []
    warnings: list[str] = []
    for path in python_files:
        file_errors, file_warnings = lint_file(path)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

    for warning in warnings:
        print(f"REVIEW: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    print(
        f"Clean-code structural lint: {len(python_files)} files, "
        f"{len(errors)} errors, {len(warnings)} review warnings."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
