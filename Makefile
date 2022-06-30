version := 0.3

MOUNT_OPTION := --mount type=bind,src=$(shell pwd)/workdir,dst=/workdir

run:
	docker run $(MOUNT_OPTION) vocoder:$(version) /usr/local/bin/python /workdir/vocoding.py

shell:
	docker run -ti $(MOUNT_OPTION) vocoder:$(version) /bin/sh
