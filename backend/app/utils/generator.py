from string import ascii_letters, digits, punctuation
from random import choice




async def async_random_string_generator(
     max_length: int,
     use_letters: bool = False,
     use_digits: bool = False,
     use_punctuation: bool = False,
     exclude: list[str] = []
) -> str:
     gen_string = ""
     
     if use_letters: gen_string += ascii_letters
     if use_digits: gen_string += digits
     if use_punctuation: gen_string += punctuation
     
     if exclude:
          for symbol in exclude:
               index = gen_string.find(symbol)
               if index != -1:
                    gen_string = gen_string[:index] + gen_string[index + 1:]
          
     return "".join([choice(gen_string) for _ in range(max_length)])



def sync_random_string_generator(
     max_length: int,
     use_letters: bool = False,
     use_digits: bool = False,
     use_punctuation: bool = False,
     exclude: list[str] = []
) -> str:
     gen_string = ""
     
     if use_letters: gen_string += ascii_letters
     if use_digits: gen_string += digits
     if use_punctuation: gen_string += punctuation
     
     if exclude:
          for symbol in exclude:
               index = gen_string.find(symbol)
               if index != -1:
                    gen_string = gen_string[:index] + gen_string[index + 1:]
          
     return "".join([choice(gen_string) for _ in range(max_length)])