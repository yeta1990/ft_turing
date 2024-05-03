import JsonParser
import Strutils

defmodule FtTuring do

  def main(args \\ []) do # \\ [] means [] by default 

    case check_valid_args(args) do
      {:help} ->
        IO.puts("usage: ft_turing [-h] jsonfile input")
        IO.puts("")
        IO.puts("positional arguments:")
        IO.puts("    jsonfile\tjson description of the machine")
        IO.puts("")
        IO.puts("    input\tinput of the machine")
        IO.puts("")
        IO.puts("optional arguments")
        IO.puts("    -h, --help\tshow this help message and exit")
        exit(:normal)
      {:error} ->
        IO.puts IO.ANSI.red() <> "Error: invalid arguments." <> IO.ANSI.reset()
        IO.puts IO.ANSI.red() <> "type `./ft_turing -h` for help" <> IO.ANSI.reset()
        System.halt(1)
      _ ->
        :done
    end

    [filename, tape] = args

    tape = tape <> "."
    case parse_json(filename) do
      {:ok, initial_status, finals, blank, transitions} -> 
        operate(tape, initial_status, 0, blank, transitions, finals)
      {:error} ->
        IO.puts("bad json")
        System.halt(1)
    end

  end


  def get_next_instruction(current_status, current_char, transitions) do

    {_, transition_value} = Enum.find(transitions, fn {key, _} ->
      to_string(key) === current_status
    end)

    next_transition = Enum.find(transition_value, fn read_step ->
       read_step[:read] == current_char
    end)
    if is_nil(next_transition) do
      IO.puts IO.ANSI.red() <> "Bad input!! No solution" <> IO.ANSI.reset()
      System.halt(1)
    end
    {next_transition.to_state, next_transition.write, next_transition.action}

  end

  defp get_next_position(current_position, next_action) do
    if next_action === "RIGHT"
    do
      current_position + 1
    else
      current_position - 1
    end
  end

  defp operate(tape, current_status, index, blank, transitions, finals) do

    if Enum.member?(finals, current_status)
    do
      print_tape_final_status(tape)
      exit(:normal)
    else
      {to_state, write, action}= get_next_instruction(current_status, String.at(tape, index), transitions) 
      print_tape_status(tape, index)
      IO.puts("(#{current_status}, #{String.at(tape, index)}) -> (#{to_state}, #{write}, #{action})")
      tape_updated = replace_char_in_strpos(tape, index, write)
      get_next_position(index, action)
      operate(tape_updated, to_state, get_next_position(index, action), blank, transitions, finals)
    end

  end

  defp check_valid_args(args) do
    cond do
      is_nil(args) ->
        {:error}
      is_help_flag(args) -> 
        {:help}
      is_expected_params(args) ->
        {:ok}
      true ->
        {:error}
    end
  end

  defp is_help_flag(args) do
    {opts, _, _} = 
      args
      |> OptionParser.parse(aliases: [h: :help], switches: [help: :boolean])

    opts[:help]
  end

  defp is_expected_params(args) do
    {_, params, _} = OptionParser.parse(args, strict: [jsonfile: :string, input: :string])
    if length(params) == 2, do: true, else: false 
  end

end


