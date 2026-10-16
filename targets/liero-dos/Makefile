# liero-dos — Turbo Pascal 7 rebuild (Free Pascal -Mtp proxy in Docker).
# Same language as the original (policy: never port to another language here).
# Toolchain image is built from compilers/Dockerfile.dos-tp7.
SLUG := liero-dos
IMAGE ?= rev:dos-tp7
BUILD := build

.PHONY: all build image clean
all: build

image:
	docker build -f ../../compilers/Dockerfile.dos-tp7 -t $(IMAGE) ../../compilers/

# NB: paths contain spaces, so the bind-mount source must be quoted.
build: image
	mkdir -p $(BUILD)
	docker run --rm -v "$(CURDIR):/src" -w /src $(IMAGE) fpc -Mtp -Fi/src/src -FE/src/build -FU/src/build /src/src/$(SLUG).pas

clean:
	rm -rf $(BUILD)/*.o $(BUILD)/*.ppu $(BUILD)/$(SLUG)
