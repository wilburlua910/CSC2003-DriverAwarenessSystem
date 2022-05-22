LIB_DIR = lib

default: pyblink

pyblink: setup.py pyblink.pyx $(LIB_DIR)/libblink.a
	python3 setup.py build_ext --inplace && rm -f pyblink.c && rm -Rf build

$(LIB_DIR)/libblink.a:
	make -C $(LIB_DIR) libblink.a

clean:
	rm *.so