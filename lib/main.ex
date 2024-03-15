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

    [filename, _instruction] = args

    case parse_json(filename) do
      {:ok} -> 
        IO.puts("ok")
      {:error} ->
        IO.puts("bad json")
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


