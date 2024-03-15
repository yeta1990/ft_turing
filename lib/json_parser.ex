import Jason

defmodule JsonParser do


    def read_file(filename) do
	  case File.read(filename) do
	    {:ok, result} -> 
	      result
	    {:error, reason} -> 
	      IO.puts(reason)
	  end
    end


	def parse_json(filename) do 
      json_string = read_file(filename)
      case decode(json_string, [{:keys, :atoms}]) do
        {:ok, decoded} ->
          scanright = decoded[:transitions][:scanright]
          Enum.each(scanright, fn transition ->
            IO.puts("Read: #{transition[:to_state]}")
          end)

          transitions = decoded.transitions
          Enum.each(transitions, fn transition -> 
            #IO.inspect transition
            {key, _value} = transition
            IO.puts(key)
          end)

        _ ->
          IO.puts("eo")
      end
	  {:ok}
	end

end
