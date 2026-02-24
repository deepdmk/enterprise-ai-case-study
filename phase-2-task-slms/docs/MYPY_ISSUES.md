# Remaining Mypy Type Issues

This document tracks mypy type errors that require more significant refactoring to fix.
These errors don't affect runtime behavior - all code works correctly.

**Current count:** 34 errors (reduced from ~50)

---

## 1. Dynamic Import in config/settings.py (6 errors)

**Files:** `config/settings.py`

```
config/settings.py:8: Library stubs not installed for "yaml"
config/settings.py:16: Argument 1 to "module_from_spec" has incompatible type "ModuleSpec | None"
config/settings.py:17: Item "None" of "ModuleSpec | None" has no attribute "loader"
config/settings.py:178: Variable "config.settings.HabitatBaseSettings" is not valid as a type
config/settings.py:178: Invalid base class "HabitatBaseSettings"
```

**Cause:** Dynamic import of `HabitatBaseSettings` from Phase 0 using `importlib`. Mypy can't trace dynamic imports.

**Fix Options:**
1. Add `# type: ignore` comments for dynamic import lines
2. Create a stub file for the Phase 0 module
3. Refactor to use conditional imports with TYPE_CHECKING guard

**Priority:** Low - works correctly at runtime

---

## 2. Protocol Type Mismatches in model_loader.py (8 errors)

**Files:** `src/shared/model_loader.py`

```
model_loader.py:142-148: Incompatible types in assignment (str/model/tokenizer to None)
model_loader.py:276,295: Return type CausalLMProtocol vs PeftModelProtocol
model_loader.py:421,427: Union type missing attributes (save_pretrained_merged, merge_and_unload)
```

**Cause:** Complex conditional model loading with Unsloth vs Transformers backends returning different model types. The Protocol classes don't fully capture all method variations.

**Fix Options:**
1. Expand `PeftModelProtocol` to include `save_pretrained_merged` as optional
2. Use `@overload` decorators for different return types
3. Add runtime type guards with `cast()` or assertions
4. Split into separate loader functions per backend

**Priority:** Medium - would improve IDE experience

---

## 3. None Attribute Access in Trainers (8 errors)

**Files:**
- `src/program2_fine_tuning/trainer_unsloth.py`
- `src/program2_fine_tuning/trainer_transformers.py`

```
trainer_unsloth.py:205-213: "None" has no attribute "save_pretrained_merged/save_pretrained"
trainer_transformers.py:260-267: "None" has no attribute methods
```

**Cause:** Variables initialized as `None` then conditionally assigned. Mypy doesn't track that these are always assigned before use in the success path.

**Fix Options:**
1. Add `assert model is not None` before method calls
2. Use early return pattern instead of conditional assignment
3. Use `Optional` with explicit None checks

**Priority:** Low - code guards against None at runtime

---

## 4. Mock Data Generator Collection Type (4 errors)

**Files:** `src/shared/mock_data_generator.py`

```
mock_data_generator.py:685-695: Collection[str] type issues with random.choice
```

**Cause:** Type inference issue with `random.choice()` on collections that could be dicts or lists.

**Fix Options:**
1. Add explicit type annotation: `input_template: str | dict[str, str] = ...`
2. Use `list()` conversion before `random.choice()`

**Priority:** Low - works correctly

---

## 5. Embedding Bridge None Access (4 errors)

**Files:** `src/shared/embedding_bridge.py`

```
embedding_bridge.py:67: Incompatible types in assignment
embedding_bridge.py:112,120: "None" has no attribute "encode/query"
```

**Cause:** Lazy initialization pattern - `self._model` and `self._collection` start as None.

**Fix Options:**
1. Add property with None check that raises if not initialized
2. Use `assert self._model is not None` before usage
3. Initialize in `__init__` instead of lazy loading

**Priority:** Low - lazy loading is intentional for performance

---

## 6. YAML Library Stubs (3 errors)

**Files:** `config/settings.py`, `src/program4_model_registry/exporter.py`, `src/shared/embedding_bridge.py`

**Cause:** Missing `types-PyYAML` in environment.

**Fix:** Run `pip install types-PyYAML` or install dev dependencies:
```bash
pip install -e ".[dev]"
```

**Priority:** Already added to `pyproject.toml` dev dependencies

---

## Quick Reference: Suppressing Specific Errors

If you need to suppress specific errors without fixing, use:

```python
# For single line:
result = some_dynamic_call()  # type: ignore[return-value]

# For multiple errors on one line:
value = obj.method()  # type: ignore[union-attr, attr-defined]

# For entire file (add at top):
# mypy: ignore-errors
```

---

## Running Mypy

```bash
# Check all src files
python -m mypy src/ --ignore-missing-imports

# Check specific file
python -m mypy src/shared/model_loader.py --ignore-missing-imports

# Show error codes (useful for targeted ignores)
python -m mypy src/ --ignore-missing-imports --show-error-codes
```
