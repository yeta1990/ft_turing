import Jason
import Strutils

defmodule JsonParser do


    def read_file(filename) do
	  case File.read(filename) do
	    {:ok, result} -> 
	      result
	    {:error, _} -> 
          IO.puts IO.ANSI.red() <> "Bad file input! Check permissions and/or json format" <> IO.ANSI.reset()
          IO.puts IO.ANSI.red() <> "type `./ft_turing -h` for help" <> IO.ANSI.reset()
          System.halt(1)
	  end
    end

	def parse_json(filename) do 
      json_string = read_file(filename)
      case decode(json_string, [{:keys, :atoms}]) do
        {:ok, decoded} ->
          IO.puts("*************************************")
          print_array("Alphabet", decoded.alphabet)
          IO.puts "Blank character : " <> decoded.blank
          print_array("States", decoded.states)
          IO.puts("Initial : #{decoded.initial}")
          print_array("Finals", decoded.finals)

          transitions = decoded.transitions
          Enum.each(transitions, fn transition -> 
            {key, value} = transition
            Enum.each(value, fn read_step ->
              IO.puts("(#{key}, #{read_step[:read]}) -> (#{read_step[:to_state]}, #{read_step[:write]}, #{read_step[:action]})")
            end)
          end)
          IO.puts("*************************************")
          {:ok, decoded.initial, decoded.finals, decoded.blank, transitions}
        _ ->
          IO.puts("Error: bad json (found in parse_json())")
          System.halt(1)
      end

	end

end
