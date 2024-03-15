defmodule FtTuring.Main do
  def main(args \\ []) do
    IO.puts("Hello world!¡!")
    args
    |> check_valid_args()
    |> response()
    #|> IO.puts()

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

    if opts[:help], do: true, else: false
  end

  defp is_expected_params(args) do
    {_, params, _} = OptionParser.parse(args, strict: [jsonfile: :string, input: :string])
    if length(params) == 2, do: true, else: false 
    #if length(params) == 2, do: [jsonfile, input] = params, else: false 
  end

  defp response({opts}) do
    case opts do
      :help -> 
        IO.puts("help")
      :ok ->
        IO.puts("OK")
      _ ->
        exit("error args!!")
    end
  end
end


