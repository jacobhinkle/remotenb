
all: build

build:
	python setup.py build

install: build
	python setup.py install

clean:
	rm -rf remotenb.egg-info
	rm -rf dist
	rm -rf build