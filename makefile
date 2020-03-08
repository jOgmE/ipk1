TARGET=python3
file_name=server.py

run:
	$(TARGET) src/$(file_name) $(PORT)
