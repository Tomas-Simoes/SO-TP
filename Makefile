# Vars
CXX = g++
CXXFLAGS = -Wall -Wextra -I./include -I./external

## Dirs
BIN_DIR = bin
OBJ_DIR = obj 

TARGET = $(BIN_DIR)/main

O_MAIN = obj/main.o
O_CONFIG = obj/config.o 

all: $(TARGET)

# Rules
$(TARGET): $(O_MAIN) $(O_CONFIG)
	@mkdir -p $(BIN_DIR) $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(O_MAIN): src/main.cpp
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $(O_MAIN)

$(O_CONFIG): src/Config.cpp
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $(O_CONFIG)

clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

.PHONY: all clean
