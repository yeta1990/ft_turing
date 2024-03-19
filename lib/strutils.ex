import IO.ANSI

defmodule Strutils do

  def replace_char_in_strpos(str, pos, new_char) do
    String.to_charlist(str)
      |> List.replace_at(pos, new_char)
      |> List.to_string
  end

  def print_tape_status(tape, index) do
    IO.write "["
    String.graphemes(tape)
    |> Enum.with_index()
    |> Enum.map(fn {x, i} ->
      if i == index do
        IO.write light_white_background() <> blue() <> x <> reset()
      else
        IO.write x
      end
      end )
    IO.write "]"
  end

end

