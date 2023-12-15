export REPOSITORY=nebulakit

PIP_COMPILE = pip-compile --upgrade --verbose --resolver=backtracking
MOCK_NEBULA_REPO=tests/nebulakit/integration/remote/mock_nebula_repo/workflows
PYTEST_OPTS ?=
PYTEST = pytest ${PYTEST_OPTS}

.SILENT: help
.PHONY: help
help:
	echo Available recipes:
	cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN { FS = ":.*?## " } { cnt++; a[cnt] = $$1; b[cnt] = $$2; if (length($$1) > max) max = length($$1) } END { for (i = 1; i <= cnt; i++) printf "  $(shell tput setaf 6)%-*s$(shell tput setaf 0) %s\n", max, a[i], b[i] }'
	tput sgr0

.PHONY: install-piptools
install-piptools:
	# pip 22.1 broke pip-tools: https://github.com/jazzband/pip-tools/issues/1617
	python -m pip install -U pip-tools setuptools wheel "pip>=22.0.3,!=22.1"

.PHONY: update_boilerplate
update_boilerplate:
	@curl https://raw.githubusercontent.com/nebulaclouds/boilerplate/master/boilerplate/update.sh -o boilerplate/update.sh
	@boilerplate/update.sh

.PHONY: setup
setup: install-piptools ## Install requirements
	pip install -r dev-requirements.in

.PHONY: fmt
fmt:
	pre-commit run ruff --all-files || true
	pre-commit run ruff-format --all-files || true

.PHONY: lint
lint: ## Run linters
	mypy nebulakit/core
	mypy nebulakit/types
	mypy --allow-empty-bodies --disable-error-code="annotation-unchecked" tests/nebulakit/unit/core
	pre-commit run --all-files

.PHONY: spellcheck
spellcheck:  ## Runs a spellchecker over all code and documentation
	codespell -L "te,raison,fo" --skip="./docs/build,./.git"

.PHONY: test
test: lint unit_test

.PHONY: unit_test_codecov
unit_test_codecov:
	$(MAKE) CODECOV_OPTS="--cov=./ --cov-report=xml --cov-append" unit_test

.PHONY: unit_test
unit_test:
	$(PYTEST) -m "not sandbox_test" tests/nebulakit/unit/ --ignore=tests/nebulakit/unit/extras/tensorflow --ignore=tests/nebulakit/unit/models ${CODECOV_OPTS} && \
		PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python $(PYTEST) tests/nebulakit/unit/extras/tensorflow ${CODECOV_OPTS}

.PHONY: test_serialization_codecov
test_serialization_codecov:
	$(MAKE) CODECOV_OPTS="--cov=./ --cov-report=xml --cov-append" test_serialization

.PHONY: test_serialization
test_serialization:
	$(PYTEST) tests/nebulakit/unit/models ${CODECOV_OPTS}


.PHONY: integration_test_codecov
integration_test_codecov:
	$(MAKE) CODECOV_OPTS="--cov=./ --cov-report=xml --cov-append" integration_test

.PHONY: integration_test
integration_test:
	$(PYTEST) tests/nebulakit/integration ${CODECOV_OPTS}

doc-requirements.txt: export CUSTOM_COMPILE_COMMAND := make doc-requirements.txt
doc-requirements.txt: doc-requirements.in install-piptools
	$(PIP_COMPILE) $<

${MOCK_NEBULA_REPO}/requirements.txt: export CUSTOM_COMPILE_COMMAND := make ${MOCK_NEBULA_REPO}/requirements.txt
${MOCK_NEBULA_REPO}/requirements.txt: ${MOCK_NEBULA_REPO}/requirements.in install-piptools
	$(PIP_COMPILE) $<

.PHONY: requirements
requirements: doc-requirements.txt ${MOCK_NEBULA_REPO}/requirements.txt ## Compile requirements

# TODO: Change this in the future to be all of nebulakit
.PHONY: coverage
coverage:
	coverage run -m pytest tests/nebulakit/unit/core nebulakit/types -m "not sandbox_test"
	coverage report -m --include="nebulakit/core/*,nebulakit/types/*"
