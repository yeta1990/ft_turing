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
	  IO.puts(json_string)
	  {:ok}
	end

end
