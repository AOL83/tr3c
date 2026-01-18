.PHONY: lint drop promote hooks

lint:
	@python scripts/lint/ascii_lint.py $(shell git ls-files)
	@files=$$(find INBOX -type f -path 'INBOX/[0-9]*/*/*' 2>/dev/null); \
	if [ -n "$$files" ]; then python scripts/lint/inbox_lint.py $$files; else echo "No INBOX drops to lint."; fi

drop:
	@./06_TEMPLATES/drop_package.sh $(TERM)

promote:
	@python scripts/promoter/promoter.py --date $(DATE)

hooks:
	@./scripts/hooks/install_hooks.sh
