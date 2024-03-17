import JsonParser

defmodule FtTuring do

  def main(args \\ []) do


    case check_valid_args(args) do
      {:help} ->
        IO.puts("help")
        exit(:normal)
      {:error} ->
        IO.puts("error")
        System.halt(1)
      _ ->
        :done
    end

    [filename, instruction] = args

    instruction = instruction <> "."
    case parse_json(filename) do
      {:ok, initial_status, finals, blank, transitions} -> 
        operate(instruction, initial_status, 0, blank, transitions, finals)
      {:error} ->
        IO.puts("bad json")
    end

  end

  def replace_char_in_strpos(str, pos, new_char) do
    String.to_charlist(str)
      |> List.replace_at(pos, new_char)
      |> List.to_string
  end

  def get_next_instruction(current_status, current_char, transitions) do

    #IO.puts(current_status)
    {transition_key, transition_value} = Enum.find(transitions, fn {key, value} ->
      to_string(key) === current_status
    end)

    next_transition = Enum.find(transition_value, fn read_step ->
       read_step[:read] == current_char
    end)
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

  defp operate(instruction, current_status, index, blank, transitions, finals) do

    if Enum.member?(finals, current_status)
    do
      exit(:normal)
    else
    {to_state, write, action}= get_next_instruction(current_status, String.at(instruction, index), transitions) 
    IO.puts("(#{current_status}, #{String.at(instruction, index)}) -> (#{to_state}, #{write}, #{action})")
    instruction_updated = replace_char_in_strpos(instruction, index, write)
    IO.puts(instruction_updated)
    get_next_position(index, action)
    operate(instruction_updated, to_state, get_next_position(index, action), blank, transitions, finals)
    end

  end

  defp check_valid_args(args) do
    cond do
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


