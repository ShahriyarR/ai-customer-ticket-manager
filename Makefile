ifdef OS
	PYTHON ?= .venv/Scripts/python.exe
	TYPE_CHECK_COMMAND ?= echo Pytype package doesn't support Windows OS
	MANAGE_PY = ${PYTHON} src/pyticket/entrypoints/web/manage.py
else
	PYTHON ?= .venv/bin/python
	TYPE_CHECK_COMMAND ?= ${PYTHON} -m pytype --config=pytype.cfg src
	MANAGE_PY = ${PYTHON} src/pyticket/entrypoints/web/manage.py
endif

SETTINGS_FILENAME = pyproject.toml
DJANGO_APP = pyticket.infrastructure.models

.PHONY: help install install-dev build format lint type-check secure test test-slow test-integration test-cov run runserver migrate makemigrations showmigrations createsuperuser shell dbshell collectstatic install-flit enable-pre-commit-hooks activate-venv create-venv check-branch-name check-conventional-commit

help:
	@echo "======================================================================"
	@echo "  Customer Ticket Classifier - Layered Architecture Makefile"
	@echo "======================================================================"
	@echo ""
	@echo "📦 SETUP COMMANDS"
	@echo "  make install-flit          Install flit build system"
	@echo "  make install                Install production dependencies"
	@echo "  make install-dev            Install development dependencies (with symlinks)"
	@echo "  make create-venv           Create virtual environment"
	@echo "  make activate-venv           Show how to activate virtual environment"
	@echo ""
	@echo "🚀 DJANGO APPLICATION COMMANDS"
	@echo "  make runserver              Start Django development server"
	@echo "  make migrate                Apply database migrations"
	@echo "  make makemigrations         Generate new migration files"
	@echo "  make showmigrations         Show migration status"
	@echo "  make createsuperuser        Create Django superuser"
	@echo "  make shell                  Open Django shell"
	@echo "  make dbshell                Open database shell"
	@echo "  make collectstatic          Collect static files"
	@echo ""
	@echo "🧪 TESTING COMMANDS"
	@echo "  make test                   Run unit tests (excludes slow/integration)"
	@echo "  make test-slow              Run slow tests"
	@echo "  make test-integration       Run integration tests"
	@echo "  make test-cov              Run tests with coverage report"
	@echo ""
	@echo "🔧 DEVELOPMENT COMMANDS"
	@echo "  make format                 Format code (black, isort, autoflake)"
	@echo "  make lint                  Check code style and quality"
	@echo "  make type-check            Run type checker (pytype)"
	@echo "  make secure                Run security checks (bandit)"
	@echo ""
	@echo "📦 BUILD COMMANDS"
	@echo "  make build                 Build wheel package"
	@echo ""
	@echo "🔨 UTILITY COMMANDS"
	@echo "  make enable-pre-commit-hooks  Install pre-commit hooks"
	@echo "  make check-branch-name      Check branch naming convention"
	@echo ""
	@echo "======================================================================"
	@echo "  Architecture: Domain → Service → Infrastructure → Entry"
	@echo "  Django App: $(DJANGO_APP)"
	@echo "  Manage.py: src/pyticket/entrypoints/web/manage.py"
	@echo "======================================================================"

# ============================================================================
# SETUP COMMANDS
# ============================================================================

install-flit:
	${PYTHON} -m pip install flit==3.8.0

install:
	${PYTHON} -m flit install --env --deps=production

install-dev:
	${PYTHON} -m flit install -s --env --deps=develop --symlink

create-venv:
	python3 -m pip install --upgrade pip
	python3 -m pip install virtualenv
	python3 -m virtualenv .venv

activate-venv:
	@echo "To activate the virtual environment, run:"
ifeq ($(OS),Windows_NT)
	@echo "  .venv\\Scripts\\activate"
else
	@echo "  source .venv/bin/activate"
endif

# ============================================================================
# DJANGO APPLICATION COMMANDS
# ============================================================================

runserver:
	@echo "🚀 Starting Django development server..."
	@echo "   API will be available at: http://127.0.0.1:8000/api/"
	@echo "   API docs will be available at: http://127.0.0.1:8000/api/docs"
	@echo ""
	${MANAGE_PY} runserver

migrate:
	@echo "📦 Applying database migrations..."
	${MANAGE_PY} migrate

makemigrations:
	@echo "📝 Generating migration files for $(DJANGO_APP)..."
	${MANAGE_PY} makemigrations $(DJANGO_APP)

makemigrations-all:
	@echo "📝 Generating migration files for all apps..."
	${MANAGE_PY} makemigrations

showmigrations:
	@echo "📋 Migration status:"
	${MANAGE_PY} showmigrations

createsuperuser:
	@echo "👤 Creating Django superuser..."
	${MANAGE_PY} createsuperuser

shell:
	@echo "🐚 Opening Django shell..."
	${MANAGE_PY} shell

dbshell:
	@echo "🗄️  Opening database shell..."
	${MANAGE_PY} dbshell

collectstatic:
	@echo "📁 Collecting static files..."
	${MANAGE_PY} collectstatic --noinput

# ============================================================================
# TESTING COMMANDS
# ============================================================================

test:
	@echo "🧪 Running unit tests (excluding slow and integration tests)..."
	${PYTHON} -m pytest -svvv -m "not slow and not integration" tests

test-slow:
	@echo "🧪 Running slow tests..."
	${PYTHON} -m pytest -svvv -m "slow" tests

test-integration:
	@echo "🧪 Running integration tests..."
	${PYTHON} -m pytest -svvv -m "integration" tests

test-cov:
	@echo "🧪 Running tests with coverage..."
	@if find tests -type f -name 'test_*.py' | grep -q .; then \
		${PYTHON} -m pytest --cov=src --cov-report=term-missing; \
		${PYTHON} -m coverage report --fail-under=96; \
	else \
		echo "⚠️  No tests found. Skipping coverage check. If tests are needed, but you don't write them, it will fail in CI checks" 1>&2; \
	fi

# ============================================================================
# DEVELOPMENT COMMANDS
# ============================================================================

format:
	@echo "🎨 Formatting code..."
	${PYTHON} -m isort src tests --force-single-line-imports --settings-file ${SETTINGS_FILENAME}
	${PYTHON} -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
	${PYTHON} -m black src tests --config ${SETTINGS_FILENAME}
	${PYTHON} -m isort src tests --settings-file ${SETTINGS_FILENAME}
	@echo "✅ Code formatted successfully!"

lint:
	@echo "🔍 Checking code style and quality..."
	${PYTHON} -m flake8 --toml-config ${SETTINGS_FILENAME} --max-complexity 5 --max-cognitive-complexity=5 src
	${PYTHON} -m black src tests --check --diff --config ${SETTINGS_FILENAME}
	${PYTHON} -m isort tests --check --diff --settings-file ${SETTINGS_FILENAME}

type-check:
	@echo "🔎 Running type checker..."
	@$(TYPE_CHECK_COMMAND)

secure:
	@echo "🔒 Running security checks..."
	${PYTHON} -m bandit -r src --config ${SETTINGS_FILENAME}

# ============================================================================
# BUILD COMMANDS
# ============================================================================

build:
	@echo "📦 Building wheel package..."
	${PYTHON} -m flit build --format wheel
	${PYTHON} -m pip install dist/*.whl
	${PYTHON} -c 'import pyticket; print(pyticket.__version__)'

# ============================================================================
# UTILITY COMMANDS
# ============================================================================

enable-pre-commit-hooks:
	@echo "🔨 Installing pre-commit hooks..."
	${PYTHON} -m pre_commit install


