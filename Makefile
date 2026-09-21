LOCAL_LIBS := \
    ../nats_contracts \
    ../polymarket_sdk

.PHONY: run-dev run-dev-local

run-dev:
	uv run python -m bot.main --nats-url nats://localhost:4222 --debug

run-dev-local:
	uv run $(foreach lib,$(LOCAL_LIBS),--with-editable $(lib)) \
		python -m bot.main --nats-url nats://localhost:4222 --debug
