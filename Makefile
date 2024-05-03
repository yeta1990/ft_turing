
all: build

build:
	docker run -v ${PWD}:/home -w /home -it --rm elixir bash -c "mix local.hex --force && \
		mix deps.get && \
		mix escript.build"

clean: 
	rm -rf deps _build mix.lock


fclean: clean
		rm -f ft_turing

.PHONY: all build clean fclean
