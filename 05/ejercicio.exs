defmodule Polimeros do

  defp type(e), do: String.upcase(e)

  defp polarity(e) do
    cond do
      String.upcase(e) == e -> :upcase
      String.downcase(e) == e -> :downcase
    end
  end

  def react(e1, e2), do: type(e1) == type(e2) and polarity(e1) != polarity(e2)

  def process(polimero) do
    processed_list = do_process(polimero, [])
    if length(processed_list) == length(polimero) do
      length(processed_list)
    else
      process(processed_list)
    end
  end

  defp do_process(list, procesadas) when length(list) < 2,
    do: Enum.reverse(list ++ procesadas)

  defp do_process([e1, e2 | demas], procesadas) do
    if react(e1, e2) do
      IO.inspect("Reaccionan #{e1} con #{e2} cuando quedan #{length(demas)} por procesar. L = #{length(procesadas)}")
      do_process(demas, procesadas)
    else
      do_process([e2 | demas], [e1 | procesadas])
    end
  end

  def remove_type(type, []), do: []

  def remove_type(type, [e | list]) do
    if type == String.upcase(e) do
      remove_type(type, list)
    else
      [e | remove_type(type, list)]
    end
  end
end

defmodule Lector do
  def read_polymer(file_name) do
    case File.read(file_name) do
      {:ok, contenido} -> {:ok, String.codepoints(String.trim(contenido))}
      {:error, tipo} -> {:error, tipo}
    end
  end

  def read_types(file_name) do
    case File.read(file_name) do
      {:error, tipo} -> {:error, tipo}
      {:ok, contenido} ->
        units = String.codepoints(String.upcase(String.trim(contenido)))
        {:ok, Enum.into(units, MapSet.new())}
    end
  end
end

# IO.puts("La cadena procesada tiene #{Polimeros.process(cadena)}")

{:ok, tipos} = Lector.read_types("datos.txt")
{:ok, cadena} = Lector.read_polymer("datos.txt")

subpolymers = Enum.map(tipos, fn tipo -> Polimeros.process(Polimeros.remove_type(tipo, cadena)) end)

IO.inspect(Enum.min(subpolymers))
