# ft_turing

## Description

`ft_turing` is a Turing machine simulator that can load instructions via a JSON file. It provides a command-line interface to interact with various Turing machines, including four "normal" machines and one universal machine. Written in Elixir

## Installation

Clone the repository:

```bash
git clone https://github.com/yeta1990/ft_turing.git
```

## Usage

```bash
./ft_turing <machine_file> <input>
```

for example:
```bash
./ft_turing machines/unary_add.json '11+1='
```


## Running Elixir Application in Docker Container
To compile and execute ft_turing within a Docker container:

1. **Pull Elixir Docker Image**: Pull the Elixir Docker image if you haven't already:
```bash
docker pull elixir
```

2. **Run Docker Container**: Launch a Docker container with the Elixir image, mounting your project directory as a volume:
```
docker run -v /path/to/your/project:/home -w /home -it --rm elixir bash
```

3. **Download dependencies and build**: In the container's shell, execute the following commands:
```bash
mix local.hex --force          # Update Hex
mix deps.get                   # Get Dependencies
mix escript.build              # Build Escript

```

4. **Execute the application**
```bash
./ft_turing <machine_file> <input>
```



## Provided machines
The project provides the following Turing machines in /machines folder:

1. unary_add.json: Adds unary numbers. Usage:
```
./ft_turing machines/unary_add.json 11+1=

```
2. 0n1n.json: decide if the input is a word of the language 0n1n. Usage:
```
./ft_turing machines/0n1n.json 0011

```

3. palindrome.json. Usage:
```
./ft_turing machines/palindrome.json 010

```

4. unary_sub.json. Substract unary numbers. Usage:
```
./ft_turing machines/unary_sub.json 11-1=

```

5. 02n.json. Decide if the input is a word of the language 02n. Usage:
```
./ft_turing machines/02n.json 0000

```

6. universal_machine.json (read the next steps before using it).

## Format of the json machine instructions


- **name**: A string representing the name of the Turing machine (unary_add in this case).
alphabet: An array listing all the symbols allowed in the Turing machine's tape.
- **blank**: A string representing the blank symbol used in the Turing machine's tape.
- **states**: An array containing all the possible states of the Turing machine. Each state is represented by a string.
- **initial**: A string indicating the initial state of the Turing machine.
- **finals**: An array listing all the final states of the Turing machine. Once the Turing machine enters any of these final states, it halts. In this project, the only final state is "HALT".
- **transitions**: An object containing transition rules for each state. Each state key maps to an array of transition objects. Each transition object describes a transition from the current state to another state based on the current tape symbol. Each transition object specifies what the Turing machine should do when it encounters a specific symbol in a specific state. For example, in the state "go_find" of unary_add.json, if the Turing machine reads the symbol "1", it stays in the "go_find" state, writes "1" to the tape, and moves the tape head to the right.
  - read: The symbol read from the tape.
  - to_state: The state to transition to if the current symbol matches the read symbol.
  - write: The symbol to write on the tape at the current position.
  - action: The action to perform after writing the symbol. It can be "LEFT", "RIGHT", or "STAY" (not present in this project, but it's a possible value in the Turing machines).



# Universal Machine
The universal Turing machine included in this project can simulate any other Turing machine. It receives the encoded instructions of other machine descriptions and the input.


## Usage with provided Tools
To use the universal machine, follow these steps:

1. **Generate Universal Machine Instructions** by executing the universal_machine_generator.py script, **or use the provided universal_machine.json** in /machines.
2. **Encode Machine Description**: Use the encode_turing_json.py script to encode the machine description (JSON file) into an encoded input for the universal machine.
3. **Run Universal Machine**: Execute the ft_turing program with the generated universal machine instructions and the encoded input.

Example with unary_add instructions as the input:

```
python universal_machine_generator.py
python encode_turing_json.py machines/unary_add.json
./ft_turing machines/universal_machine.json 'A¡?A1A1>?A.A.>?A+A+>?A=B.<?B1C.<?C1C1<?C+W1<!11+1111='
```


